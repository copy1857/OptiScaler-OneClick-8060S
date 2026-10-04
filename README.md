# 授權與來源（請先閱讀）

這是個人製作的測試工具，僅供少數熟人測試，**不是任何廠商的官方產品**，在 AMD Radeon 8060S 上實測，其他顯卡未驗證。
使用前請先退出遊戲；不要用在有反作弊的線上遊戲。所有變更都會備份，可用「還原」復原。

## 內含元件
| 元件 | 來源 | 授權 |
|---|---|---|
| OptiScaler（TheAutomatic/dlss-5-amd-project 1.9.9.1 版本體） | https://github.com/TheAutomatic/dlss-5-amd-project ／ 上游 https://github.com/optiscaler/OptiScaler | GPL-3.0（見 Licenses/OptiScaler_LICENSE.txt，原始碼見上列網址） |
| AMD FidelityFX（FSR 4.1.1） | AMD GPUOpen | 見 Licenses/FidelityFX_*_LICENSE.md |
| Intel XeSS／XeFG／XeLL | Intel | 見 Licenses/XeSS_LICENSE.txt |
| DirectX Agility SDK（D3D12Core.dll） | Microsoft | 見 Licenses/DirectX_LICENSE.txt |
| dlssg-to-fsr3（Nukem） | https://github.com/Nukem9/dlssg-to-fsr3 | GPL-3.0 |
| OptiPatcher | https://github.com/optiscaler/OptiPatcher | MIT |
| DLSS Enabler（Arturs） | https://www.nexusmods.com/site/mods/757 | 作者未公開散布條款（授權不明） |
| XeFGUnlock 1.1.4 | 隨社群版 OptiScaler 套件流傳 | 作者與授權不明 |
| NVIDIA Streamline／DLSS 執行檔 | NVIDIA Streamline SDK | NVIDIA 授權（用於模組時有爭議） |
| experimental_lighting 著色器 | 社群版 DLSS5 套件 | 授權不明 |

授權不明的元件由發行者自行承擔風險保留，若權利人要求會移除。

## 不包含：DLSS5 runtime 與權重
社群版 DLSS5 的 AMD runtime 是 Daniel Blanco 的作品（https://github.com/danielblnc/DLSS-NR-on-AMD），授權禁止放進其他工具或安裝包；
權重必須用你自己的 NVIDIA nvngx_dlssnr.dll（支援 DLSS 5 的遊戲內附）轉換。請在工具上方按「DLSS5 未設定」，依三個步驟從官方取得後匯入。
未設定前，工具照樣能安裝 FSR 4.1.1 與補幀。

## 更新
工具啟動時會檢查 GitHub 上的新版本（https://github.com/copy1857/OptiScaler-OneClick-8060S/releases），有新版會在右上角出現「有新版本」，按下後下載差異更新並自動重新啟動。
