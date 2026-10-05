"""Automatic evaluation of a problem report (diagnostics.collect): every rule looks at the collected data, and each
finding names what is abnormal, the evidence, and the fix. Used by the tool (shown to the tester right after the report
is made) and by scripts/fetch_reports.py (every report pulled from GitHub or a file).

Thresholds come from measurements on this Radeon 8060S at 55 W (outputs/witcher3-perf-20261005): DLSS5 0.5.1 / 0.6.0
needs ~25 ms per run at 960x540 input, the game waits ~12-30 ms for its own frame; at a 20 W battery TDP both triple.
"""
import re

HIGH, MID, LOW = '高', '中', '低'
OUR_PREFIX = ('optiscaler', 'dlssnr', 'amd_fidelityfx', 'libxess', 'libxell', 'd3d12_optiscaler', 'nvngx', 'sl.')
FOREIGN_PROXIES = {'dinput8.dll': 'REFramework／ASI 載入器', 'version.dll': 'Daniel 或其他代理', 'winmm.dll': '其他代理 DLL',
                   'd3d12.dll': '其他代理 DLL', 'dxgi.dll': 'ReShade 或其他 OptiScaler'}  # ReShade itself is supported (LoadReshade)
MS_PER_MPIX = 48.0  # DLSS5 network time per input megapixel at 55 W (25 ms / 0.52 MP)


def _pixels(res):
    m = re.fullmatch(r'(\d+)x(\d+)', str(res or ''))
    return int(m.group(1)) * int(m.group(2)) if m else None


def finding(fid, severity, title, evidence, fix, action=None):
    return {'id': fid, 'severity': severity, 'title': title, 'evidence': evidence, 'fix': fix, 'action': action}


def analyze(d):
    out = []
    system, tool, inst = d.get('system') or {}, d.get('tool') or {}, d.get('install') or {}
    perf = d.get('performance') or {}; dl, fg, m = perf.get('dlss5') or {}, perf.get('fg') or {}, perf.get('measured') or {}

    # power / TDP
    for pw, when in ((system.get('power'), '產生報告時'), (m.get('power'), '測量時')):
        if not pw: continue
        if pw.get('ac') is False or pw.get('battery_saver') or (pw.get('battery_pct') is not None and pw['battery_pct'] < 20):
            state = '用電池' if pw.get('ac') is False else '省電模式' if pw.get('battery_saver') else f"電量 {pw['battery_pct']}%"
            out.append(finding('power', HIGH, f'{when}{state}：TDP 很可能被降低',
                               f"電源 {pw}", '插上電源、關閉省電模式，並在掌機軟體把 TDP 設回正常值（8060S 約 55 W）；'
                               '20 W 時幀時間約為 3 倍。'))
            break

    # DLSS5: game still on an older runtime than the tool's selection
    chosen = (tool.get('dlss5') or {}).get('version')
    ran = (dl.get('version') or '').lstrip('v')
    if chosen and ran and ran != chosen and inst:
        out.append(finding('dlss5_outdated', MID, f'這款遊戲的 DLSS5 還是 {ran}，工具目前選的是 {chosen}',
                           f"最近一次遊戲 log：v{ran}（build {dl.get('build')}）", '在工具選這款遊戲按「套用更新」，或在 DLSS5 視窗切換版本後選「是」套用。',
                           action='refresh'))
    # DLSS5 slower than this hardware should be
    px = _pixels(dl.get('input'))
    if dl.get('network_ms_median') and px:
        expect = MS_PER_MPIX * px / 1e6
        if dl['network_ms_median'] > max(1.6 * expect, expect + 8):
            out.append(finding('dlss5_slow', MID, 'DLSS5 每次運算比正常慢',
                               f"{dl['network_ms_median']} ms（輸入 {dl['input']}，55 W 時約 {expect:.0f} ms）",
                               '先確認插電與 TDP；仍慢就把 DLSS5 比例降一級（例如 75%→50%）。'))
    # real frame rate too low for frame generation
    real = (m.get('real') or {}).get('avg_fps') or fg.get('real_fps')
    if real and inst.get('mode') in ('native', 'proxy') and real < 20:
        out.append(finding('real_fps_low', MID, f'補幀前只有 {real} FPS：補幀會有明顯殘影與延遲',
                           f"真實畫面 {real} FPS（{'實測' if m.get('real') else 'XeFG log'}）",
                           '把 DLSS5 比例降一級或關閉、降低遊戲光追／畫質，或補幀改成 2 倍；補幀前至少 30 FPS 效果較好。'))
    # measured stutter and latency
    o = m.get('output') or {}
    # stutter = sudden 1% low drops at given moments (a steady low 1% low only feels slow, see real_fps_low)
    stt = m.get('stutter') or {}
    if stt.get('count'):
        sev = HIGH if stt['severe'] >= 3 else MID if stt['severe'] or stt['count'] >= 3 else LOW
        pts = '、'.join(f"{e['t_s']}s（降 {e['drop_pct']}%）" for e in stt['events'][:6])
        out.append(finding('stutter', sev, f"有 {stt['count']} 次卡頓（1% low 突然下降 50% 以上，嚴重 {stt['severe']} 次）",
                           f"平常 1% low {stt['usual_low_fps']} FPS；時間點 {pts}",
                           '同一位置重複出現多半是著色器編譯或讀取，跑第二次再測；每次都出現時降低 DLSS5 比例或畫質，'
                           '並確認插電與 TDP。'))
    for lt in m.get('latency') or []:
        if lt.get('metric') in ('MsPCLatency', 'DisplayLatency') and lt.get('avg_ms', 0) > 100:
            out.append(finding('latency', MID, f"延遲偏高：平均 {lt['avg_ms']} ms",
                               f"{lt['label']} 平均 {lt['avg_ms']} ms、95% {lt['p95_ms']} ms",
                               '補幀倍數降一級、DLSS5 比例降低或關閉；動作遊戲建議補幀前 FPS 至少 40。'))
            break

    # crashes
    for c in (d.get('crashes') or [])[:3]:
        mod = (c.get('module') or '').lower()
        if not mod: continue
        if mod.startswith(OUR_PREFIX) or mod in ('dxgi.dll', 'winmm.dll', 'version.dll', 'd3d12.dll'):
            out.append(finding('crash_ours', HIGH, f"閃退發生在外掛元件 {c['module']}",
                               f"{c['time']} 錯誤碼 {c.get('exception')}", '先改用「純 FSR 4.1.1」方案確認；仍閃退就按「還原」，把這份報告回報。'))
        elif mod.startswith(('amdxc', 'amdx', 'atiumd', 'amdvlk')):
            out.append(finding('crash_driver', HIGH, f"閃退發生在 AMD 驅動 {c['module']}",
                               f"{c['time']} 錯誤碼 {c.get('exception')}", '更新或重新安裝 AMD Adrenalin 驅動；DLSS5 比例先降低。'))
        else:
            out.append(finding('crash_game', MID, f"遊戲閃退（{c['module']}）",
                               f"{c['time']} 錯誤碼 {c.get('exception')}", '若安裝工具前不會閃退，先改用「純 FSR 4.1.1」測試，並移除其他模組。'))
        break

    # OptiScaler not loaded / foreign proxies / missing FG inputs
    if inst and not d.get('logs'):
        out.append(finding('not_loaded', HIGH, 'OptiScaler 沒有被遊戲載入', '遊戲資料夾沒有 OptiScaler.log',
                           '確認遊戲沒有防作弊；在相容說明看建議的代理檔名，必要時還原後換方案再裝。'))
    installed = {p.lower() for p in (d.get('installed_files') or [])}
    foreign = [f['path'] for f in (d.get('folder') or []) if f['path'].lower() in FOREIGN_PROXIES and f['path'].lower() not in installed]
    if foreign:
        out.append(finding('foreign_mods', MID, '遊戲資料夾有不是本工具裝的代理／外掛',
                           '、'.join(f'{p}（{FOREIGN_PROXIES[p.lower()]}）' for p in foreign),
                           '會和 OptiScaler 搶載入；用「還原」清理（Daniel 的 DLSS5 會先匯入工具），或手動移到別處。'))
    text = '\n'.join(l for lg in (d.get('logs') or []) for l in (lg.get('tail') or []) + (lg.get('problems') or []))
    if text.count('Depth or Velocity is not ready') >= 30:
        out.append(finding('fg_inputs', MID, '補幀一直拿不到深度／動態向量',
                           f"log 出現 {text.count('Depth or Velocity is not ready')} 次 Depth or Velocity is not ready",
                           '遊戲內要開 DLSS（或 XeSS）升頻；原生補幀方案還要開遊戲的 DLSS 幀生成。過場動畫與選單出現少量屬正常。'))
    if 'Back buffers have outstanding references' in text or 'Preventing flag change for XeFG' in text:
        out.append(finding('xefg_resize', HIGH if 'outstanding references' in text else LOW,
                           '切換全螢幕／無邊框或解析度時，XeFG 補幀失敗（遊戲可能直接關閉）',
                           'log：XeFG Log: Back buffers have outstanding references／Preventing flag change for XeFG',
                           '先在遊戲設定選好「無邊框視窗」與解析度並重開遊戲，之後不要在遊戲中切換顯示模式；'
                           '一定要切換時，先按 Home 開 OptiScaler 選單把補幀關掉再切。也避免使用會切換全螢幕的按鍵（F11、Alt+Enter）。'))
    if inst.get('nr_model_scale') and not (tool.get('dlss5') or {}).get('ready'):
        out.append(finding('dlss5_missing', LOW, '方案有開 DLSS5，但工具尚未設定 DLSS5', 'DLSS5 未設定',
                           '點右上角 DLSS5 標籤依指示設定；未設定前 DLSS5 會自動關閉。'))
    refresh = system.get('refresh_hz'); limit = inst.get('fps_limit')
    if refresh and limit and abs((refresh - 3) - limit) > 2:
        out.append(finding('refresh_changed', LOW, f'螢幕更新率變了（現在 {refresh} Hz，FPS 上限仍是 {limit}）',
                           f'安裝時 {inst.get("display_refresh_hz")} Hz', '按「套用更新」重新計算 FPS 上限。', action='refresh'))
    used = m.get('multiplier')
    if used and inst.get('multiplier') and inst.get('mode') in ('native', 'proxy') and used != inst['multiplier']:
        out.append(finding('multiplier_changed', LOW, f"補幀實際是 {used} 倍，工具安裝的是 {inst['multiplier']} 倍",
                           '遊戲內 OptiScaler 選單（Home）改過補幀倍數', '這是你在遊戲裡選的就不用處理；想回到工具的設定，在工具按「套用更新」。',
                           action='refresh'))
    order = {HIGH: 0, MID: 1, LOW: 2}
    return sorted(out, key=lambda f: order[f['severity']])


def lines(findings):
    if not findings: return ['- 沒有發現異常']
    return [f"- 【{f['severity']}】{f['title']}　依據：{f['evidence']}　→ 建議：{f['fix']}" for f in findings]
