"""GitHub Action: read a [診斷回報] issue, run the tool's rules (diag_rules.py, same file the tool uses) on the report's
JSON, and post / update one reply with the findings, the fixes and a short performance summary.

Labels: 自動判斷 on every report; 需深入分析 when the rules cannot fully explain it (no finding, a crash or "not loaded"
whose cause the rules cannot name, or a described problem with only minor findings) - the scheduled deep analysis
works through those; 需補資料 when the issue has no report data.
Run locally: DRY_RUN=1 REPO=owner/name ISSUE_NUMBER=1 python analyze_issue.py  (prints instead of posting).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import diag_rules

MARKER = '<!-- oneclick-auto-diagnosis -->'
UNKNOWN_CAUSE = {'crash_game', 'crash_ours', 'not_loaded'}
REPO, NUMBER, DRY = os.environ['REPO'], os.environ['ISSUE_NUMBER'], bool(os.environ.get('DRY_RUN'))


def gh(*args, data=None):
    r = subprocess.run(['gh', *args], capture_output=True, text=True, encoding='utf-8', input=data)
    if r.returncode: raise SystemExit(f'gh {args[:3]} failed: {r.stderr.strip()[:300]}')
    return r.stdout


def report_json(body):
    m = re.search(r'```json\n(.*?)\n```', (body or '').replace('\r\n', '\n'), re.S)
    if not m: return None
    try: return json.loads(m.group(1))
    except ValueError: return None


def summary(d):
    """A few lines a tester can read at a glance."""
    out = []
    sysi, inst, tool = d.get('system') or {}, d.get('install') or {}, d.get('tool') or {}
    gpu = ', '.join(f"{g.get('name')}（驅動 {g.get('driver')}）" for g in sysi.get('gpus') or [])
    pw = sysi.get('power') or {}
    out.append(f"- 遊戲：{(d.get('game') or {}).get('name')}　工具 {tool.get('version')}　{gpu}")
    if pw: out.append(f"- 電源：{'插電' if pw.get('ac') else '電池' if pw.get('ac') is False else '未知'}"
                      + (f"，電量 {pw.get('battery_pct')}%" if pw.get('battery_pct') is not None else '')
                      + ('，省電模式' if pw.get('battery_saver') else ''))
    if inst: out.append(f"- 方案：{inst.get('mode')}、補幀 {inst.get('fg_engine')} {inst.get('multiplier')} 倍、DLSS5 比例 {inst.get('nr_model_scale')}")
    perf = d.get('performance') or {}; m = perf.get('measured') or {}
    if m:
        o, r = m.get('output') or {}, m.get('real') or {}
        out.append(f"- 實測 {m.get('seconds')} 秒：補幀後 {o.get('avg_fps')} FPS（1% low {o.get('low1_fps')}），"
                   f"補幀前 {r.get('avg_fps')} FPS（{r.get('method', '')}）")
        for lt in m.get('latency') or []: out.append(f"- {lt.get('label')}：平均 {lt.get('avg_ms')} ms，95% {lt.get('p95_ms')} ms")
        st = m.get('stutter') or {}
        if st: out.append(f"- 卡頓：{st.get('count', 0)} 次（嚴重 {st.get('severe', 0)}）" +
                          ('，時間點 ' + '、'.join(f"{e['t_s']}s 降 {e['drop_pct']}%" for e in st.get('events', [])[:6]) if st.get('count') else ''))
    dl = perf.get('dlss5') or {}
    if dl.get('network_ms_median'):
        out.append(f"- DLSS5 {dl.get('version')}：每次運算 {dl['network_ms_median']} ms（輸入 {dl.get('input')}）")
    return out


def main():
    issue = json.loads(gh('issue', 'view', NUMBER, '-R', REPO, '--json', 'title,body,labels'))
    d = report_json(issue.get('body'))
    labels = ['自動判斷']
    if not d:
        text = (f"{MARKER}\n### 自動判斷\n找不到報告資料。請在工具按「回報問題」→「產生報告」→「複製並開啟 GitHub 回報」，"
                "把整份報告（含最後的「完整資料（JSON）」）貼進這個 issue 的內容。")
        labels.append('需補資料')
    else:
        found = diag_rules.analyze(d)
        deep = (not found or any(f['id'] in UNKNOWN_CAUSE for f in found)
                or (d.get('description') and all(f['severity'] == diag_rules.LOW for f in found)))
        lines = [MARKER, '### 自動判斷（工具內建規則）', ''] + diag_rules.lines(found) + ['', '### 摘要'] + summary(d)
        if deep:
            lines += ['', '> 這份回報有規則無法完整判斷的部分，已轉給進一步分析，會再回覆。']
            labels.append('需深入分析')
        lines += ['', f"<sub>報告 {d.get('key')}｜判斷規則 diag_rules.py｜這則留言會在 issue 內容更新時自動重新判斷</sub>"]
        text = '\n'.join(lines)
    if DRY:
        print(text); print('labels:', labels); return
    mine = [c for c in json.loads(gh('api', f'repos/{REPO}/issues/{NUMBER}/comments', '--paginate')) if MARKER in (c.get('body') or '')]
    if mine: gh('api', '-X', 'PATCH', f"repos/{REPO}/issues/comments/{mine[0]['id']}", '-f', f'body={text}')
    else: gh('issue', 'comment', NUMBER, '-R', REPO, '--body-file', '-', data=text)
    stale = [l['name'] for l in issue.get('labels') or [] if l['name'] in ('需補資料',) and l['name'] not in labels]
    gh('issue', 'edit', NUMBER, '-R', REPO, '--add-label', ','.join(labels), *(['--remove-label', ','.join(stale)] if stale else []))
    print('replied', NUMBER, labels)


if __name__ == '__main__':
    main()
