# 授權與來源（請先閱讀）

這是個人製作的測試工具，僅供少數熟人測試，**不是任何廠商的官方產品**，在 AMD Radeon 8060S 上實測，其他顯卡未驗證。
使用前請先退出遊戲。有反作弊的線上遊戲（例如 Battle.net 遊戲）裝外掛可能被封鎖帳號，工具會先要求同意免責聲明，風險由使用者自行承擔；EasyAntiCheat／BattlEye 的遊戲不提供安裝。所有變更都會備份，可用「還原」復原。

## 內含元件
| 元件 | 來源 | 授權 |
|---|---|---|
| OptiScaler（TheAutomatic/dlss-5-amd-project 1.12.2 版本體） | https://github.com/TheAutomatic/dlss-5-amd-project ／ 上游 https://github.com/optiscaler/OptiScaler | GPL-3.0（見 Licenses/OptiScaler_LICENSE.txt，原始碼見上列網址） |
| OptiScaler 0.9.4 官方簽章版（SignPath Foundation 簽章；只給只載入簽章 DLL 的遊戲：Diablo II: Resurrected、Diablo IV） | https://github.com/optiscaler/OptiScaler/releases/tag/v0.9.4（Optiscaler_0.9.4-final.20260718._MM.7z，sha256 575cb4df866116093df75af607e37fd70e10f5163e0f23fd5c804142e80ef0ad；只取出 OptiScaler.dll 與 OptiScaler.ini，未修改） | GPL-3.0（見 Licenses/OptiScaler_LICENSE.txt） |
| AMD FidelityFX（FSR SDK 2.3.0：升頻 4.1.1、補幀 4.0.1） | AMD GPUOpen | 見 Licenses/FidelityFX_*_LICENSE.md |
| Intel XeSS／XeFG／XeLL | Intel | 見 Licenses/XeSS_LICENSE.txt |
| DirectX Agility SDK（D3D12Core.dll） | Microsoft | 見 Licenses/DirectX_LICENSE.txt |
| dlssg-to-fsr3（Nukem） | https://github.com/Nukem9/dlssg-to-fsr3 | GPL-3.0 |
| OptiPatcher | https://github.com/optiscaler/OptiPatcher | MIT |
| REFramework（只有 Capcom RE 引擎遊戲安裝時才下載，不在安裝包內） | https://github.com/praydog/REFramework-nightly | MIT |
| Luma（只有原生沒有升頻、Luma 相容表列為可用的遊戲安裝時才下載，不在安裝包內） | https://github.com/Filoppi/Luma-Framework（作者 Filippo Tarpini 等） | Custom MIT（需標示作者，商業用途須先取得授權） |
| Luma 相容表（luma_games.json，由 Luma wiki 整理並加上本機實測結果） | https://github.com/Filoppi/Luma-Framework/wiki | 依 Luma 專案 |
| Arise-SDK（只有 Tales of Arise 走 Luma 方案時才下載，不在安裝包內） | https://github.com/emoose/Arise-SDK | GPL-3.0 |
| Magpie FSR 4.1.1 版（A-ENTROPY/magpie-dlss5-amd v0.6.8.5-amd-rdna3，Blinue/Magpie 的分支；只有沒有升頻的遊戲第一次開始遊戲時才下載並核對 sha256，不在安裝包內） | https://github.com/A-ENTROPY/magpie-dlss5-amd ／ 上游 https://github.com/Blinue/Magpie | GPL-3.0 |
| Ludusavi v0.31.0（mtkennerly/ludusavi；存檔備份用，第一次開啟存檔備份時才從官方 Release 下載並核對 sha256，不在安裝包內） | https://github.com/mtkennerly/ludusavi | MIT |
| Ludusavi 存檔位置表（ludusavi-manifest，內容來自 PCGamingWiki；執行時下載，不在安裝包內） | https://github.com/mtkennerly/ludusavi-manifest ／ https://www.pcgamingwiki.com | 倉庫 MIT；位置資料 CC BY-NC-SA 3.0 |
| PresentMon（只有按「測量效能」時才下載，不在安裝包內） | https://github.com/GameTechDev/PresentMon | MIT |
| PawnIO 2.2.0 官方安裝程式（pawnio/，未修改；只有玩家在掌機面板同意後才安裝，可在 Windows「應用程式」移除；解除安裝 AURORA 不會移除它） | https://pawnio.eu ／ 原始碼 https://github.com/namazso/PawnIO/tree/2.2.0 | GPL-2.0-or-later，附獨立程式的例外條款；安裝程式註明可未經修改再散布（見 pawnio/原始碼與授權.md） |
| PawnIO.Modules 0.2.11 官方簽章版（pawnio/ 內 RyzenSMU.bin、LpcIO.bin、LpcACPIEC.bin，未修改；掌機面板調 TDP、風扇、電池保護用） | https://github.com/namazso/PawnIO.Modules/tree/0.2.11 | LGPL-2.1（見 pawnio/COPYING） |
| SISR 與 VIIPER（Steam 手把給非 Steam 遊戲用；由玩家自己用 SISR 的安裝程式裝到 %LOCALAPPDATA%\SISR，AURORA 只呼叫它、在升級專區從官方 Release 更新，不在安裝包內） | https://github.com/Alia5/SISR ／ https://github.com/Alia5/VIIPER | GPL-3.0 |
| SCSKiller 著色器預編譯（scskiller/ 內官方可攜版，未修改；第一次啟動時安裝到 %LOCALAPPDATA%\SCSKiller-Portable，AURORA 只呼叫它的命令列） | https://github.com/BlueHeisenberg/SCSKiller（對應原始碼見 scskiller/原始碼與授權.md） | GPL-3.0-or-later＋附加許可（見 scskiller/LICENSE、LICENSE-EXCEPTION.txt、THIRD-PARTY-NOTICES.md） |
| DLSS Enabler（Arturs） | https://www.nexusmods.com/site/mods/757 | 作者未公開散布條款（授權不明） |
| XeFGUnlock 1.1.4 | 隨社群版 OptiScaler 套件流傳 | 作者與授權不明 |
| NVIDIA Streamline／DLSS 執行檔 | NVIDIA Streamline SDK | NVIDIA 授權（用於模組時有爭議） |
| experimental_lighting 著色器 | 社群版 DLSS5 套件 | 授權不明 |
| 一鍵修改器的手把與功能圖示（trainer-art/，AI 生成的非官方示意圖；Steam Controller 2 圖由使用者提供；來源見 trainer-art/provenance.json） | 本工具製作 | 隨本工具 |
| NumPy（修改器找數值用） | https://numpy.org | BSD-3-Clause（見 _internal/numpy-*.dist-info/licenses） |
| Noto Sans TC 字型（fonts/NotoSansTC-VF.ttf，2.004 版，未修改；Big Picture 介面用，沒裝的電腦會自動裝到目前使用者） | Adobe／Google（Source Han Sans／Noto CJK）https://github.com/notofonts/noto-cjk | SIL Open Font License 1.1（見 fonts/OFL.txt） |
| AURORA 的 Rust 元件：aurora-app.exe（大圖模式、掌機面板、常駐）、aurora-dlboost.exe（下載加速提權小幫手）、aurora-hw.exe（掌機面板的提權硬體小幫手）、_internal/aurora_core.pyd（手把、掃描、記憶體搜尋等核心） | 本工具製作（原始碼在本工具倉庫 rust/） | 隨本工具；使用的第三方 Rust 套件（egui／eframe、wgpu、windows-rs、PyO3 等）授權全文見 Licenses/Rust-third-party-licenses.txt（含各套件的 LICENSE／NOTICE、著作權人與來源；egui 內建字型的 OFL／Ubuntu Font License 也在內） |
| 大圖模式開機影片（intro/，由使用者以 PixVerse 製作的影片轉成畫格與音效；來源見 intro/intro.json） | 使用者提供 | 隨本工具 |
| 介面背景圖（ui-art/，本工具以程式產生；來源見 ui-art/provenance.json）與 Steam 圖示（steam-art/，來源見 steam-art/art.json） | 本工具製作 | 隨本工具 |

ROG 掌機的 ATK ACPI 指令格式參考 G-Helper（https://github.com/seerge/g-helper，GPL-3.0）的公開做法，AURORA 自己撰寫，沒有收錄它的程式碼。

授權不明的元件由發行者自行承擔風險保留，若權利人要求會移除。

## 一鍵修改器（只限單機）
修改器由本工具自己從遊戲外部讀寫記憶體，不改遊戲檔案、不注入、不碰畫面輸出；有反作弊的遊戲不提供，有線上功能的遊戲要先同意只在單機使用。修改的數值可能跟著存檔，建議先備份存檔。
「風靈月影」修改器（https://flingtrainer.com）不在安裝包內：只有在選單打開它的開關時，才從官網下載那一款到本機，著作與授權屬原作者。

## 不包含：DLSS5 runtime 與權重
社群版 DLSS5 的 AMD runtime 是 Daniel Blanco 的作品（https://github.com/danielblnc/DLSS-NR-on-AMD），授權禁止放進其他工具或安裝包；
權重必須用你自己的 NVIDIA nvngx_dlssnr.dll（支援 DLSS 5 的遊戲內附）轉換。請在工具右上方按「設定 DLSS5」，按「下載 Daniel 安裝程式」
從他的官方 GitHub 下載到「下載」資料夾，工具偵測到後會自動完成安裝與匯入（會自動搜尋你電腦裡的 nvngx_dlssnr.dll）。
未設定前，工具照樣能安裝 FSR 4.1.1 與補幀。

## Rust 元件與退回
- 大圖模式預設用新版（Rust，aurora-app.exe）；沒有在 40 秒內出現畫面就自動改用舊版並說明原因。想一直用舊版：桌面版 ☰ 選單 →「大圖模式：新版」按一下切成舊版（會記住）。
- 環境變數 AURORA_NO_RUST=1：只讓 aurora_core.pyd 的核心（手把、遊戲庫掃描、記憶體搜尋、下載、風靈月影與 SCSKiller 的部分）改回 Python 舊實作；不影響大圖模式選哪一版，也不影響下載加速的提權小幫手（aurora-dlboost.exe）。

## 更新
工具啟動時會檢查 GitHub 上的新版本（https://github.com/copy1857/OptiScaler-OneClick-8060S/releases），有新版會在右上角出現「有新版本」，按下後下載差異更新並自動重新啟動。
