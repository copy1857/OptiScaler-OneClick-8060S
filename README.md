# 授權與來源（請先閱讀）

這是個人製作的測試工具，僅供少數熟人測試，**不是任何廠商的官方產品**，在 AMD Radeon 8060S 上實測，其他顯卡未驗證。
使用前請先退出遊戲。有反作弊的線上遊戲（例如 Battle.net 遊戲）裝外掛可能被封鎖帳號，工具會先要求同意免責聲明，風險由使用者自行承擔；EasyAntiCheat／BattlEye 的遊戲不提供安裝。所有變更都會備份，可用「還原」復原。

## 內含元件
| 元件 | 來源 | 授權 |
|---|---|---|
| OptiScaler（TheAutomatic/dlss-5-amd-project 1.10.0 版本體） | https://github.com/TheAutomatic/dlss-5-amd-project ／ 上游 https://github.com/optiscaler/OptiScaler | GPL-3.0（見 Licenses/OptiScaler_LICENSE.txt，原始碼見上列網址） |
| OptiScaler 0.9.4 官方簽章版（SignPath Foundation 簽章；只給只載入簽章 DLL 的遊戲：Diablo II: Resurrected、Diablo IV） | https://github.com/optiscaler/OptiScaler/releases/tag/v0.9.4（Optiscaler_0.9.4-final.20260718._MM.7z，sha256 575cb4df866116093df75af607e37fd70e10f5163e0f23fd5c804142e80ef0ad；只取出 OptiScaler.dll 與 OptiScaler.ini，未修改） | GPL-3.0（見 Licenses/OptiScaler_LICENSE.txt） |
| AMD FidelityFX（FSR 4.1.1） | AMD GPUOpen | 見 Licenses/FidelityFX_*_LICENSE.md |
| Intel XeSS／XeFG／XeLL | Intel | 見 Licenses/XeSS_LICENSE.txt |
| DirectX Agility SDK（D3D12Core.dll） | Microsoft | 見 Licenses/DirectX_LICENSE.txt |
| dlssg-to-fsr3（Nukem） | https://github.com/Nukem9/dlssg-to-fsr3 | GPL-3.0 |
| OptiPatcher | https://github.com/optiscaler/OptiPatcher | MIT |
| REFramework（只有 Capcom RE 引擎遊戲安裝時才下載，不在安裝包內） | https://github.com/praydog/REFramework-nightly | MIT |
| Luma（只有原生沒有升頻、Luma 相容表列為可用的遊戲安裝時才下載，不在安裝包內） | https://github.com/Filoppi/Luma-Framework（作者 Filippo Tarpini 等） | Custom MIT（需標示作者，商業用途須先取得授權） |
| Luma 相容表（luma_games.json，由 Luma wiki 整理並加上本機實測結果） | https://github.com/Filoppi/Luma-Framework/wiki | 依 Luma 專案 |
| Arise-SDK（只有 Tales of Arise 走 Luma 方案時才下載，不在安裝包內） | https://github.com/emoose/Arise-SDK | GPL-3.0 |
| PresentMon（只有按「測量效能」時才下載，不在安裝包內） | https://github.com/GameTechDev/PresentMon | MIT |
| DLSS Enabler（Arturs） | https://www.nexusmods.com/site/mods/757 | 作者未公開散布條款（授權不明） |
| XeFGUnlock 1.1.4 | 隨社群版 OptiScaler 套件流傳 | 作者與授權不明 |
| NVIDIA Streamline／DLSS 執行檔 | NVIDIA Streamline SDK | NVIDIA 授權（用於模組時有爭議） |
| experimental_lighting 著色器 | 社群版 DLSS5 套件 | 授權不明 |
| Noto Sans TC 字型（fonts/NotoSansTC-VF.ttf，2.004 版，未修改；Big Picture 介面用，沒裝的電腦會自動裝到目前使用者） | Adobe／Google（Source Han Sans／Noto CJK）https://github.com/notofonts/noto-cjk | SIL Open Font License 1.1（見 fonts/OFL.txt） |

授權不明的元件由發行者自行承擔風險保留，若權利人要求會移除。

## 不包含：DLSS5 runtime 與權重
社群版 DLSS5 的 AMD runtime 是 Daniel Blanco 的作品（https://github.com/danielblnc/DLSS-NR-on-AMD），授權禁止放進其他工具或安裝包；
權重必須用你自己的 NVIDIA nvngx_dlssnr.dll（支援 DLSS 5 的遊戲內附）轉換。請在工具右上方按「設定 DLSS5」，按「下載 Daniel 安裝程式」
從他的官方 GitHub 下載到「下載」資料夾，工具偵測到後會自動完成安裝與匯入（會自動搜尋你電腦裡的 nvngx_dlssnr.dll）。
未設定前，工具照樣能安裝 FSR 4.1.1 與補幀。

## 更新
工具啟動時會檢查 GitHub 上的新版本（https://github.com/copy1857/OptiScaler-OneClick-8060S/releases），有新版會在右上角出現「有新版本」，按下後下載差異更新並自動重新啟動。
