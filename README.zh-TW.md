# Fishing Game Source｜Cocos 捕魚遊戲與金幣大廳原始碼

[簡體中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

<p align="center">
  <img src="https://img.shields.io/badge/Client-Cocos%20Creator-blue?style=flat-square" alt="Cocos Creator 捕魚遊戲客戶端">
  <img src="https://img.shields.io/badge/Language-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript 遊戲腳本">
  <img src="https://img.shields.io/badge/Platform-iOS%20%7C%20Android-blueviolet?style=flat-square" alt="iOS 與 Android 捕魚遊戲">
</p>

**Fishing Game Source** 是一個 Cocos 捕魚遊戲原始碼專案，包含捕魚金幣大廳、經典模式、比賽模式、玉石場、BOSS 玩法、休閒小遊戲及相關系統模組。倉庫提供客戶端資源與腳本、服務端工具、專案文件和真實產品截圖。

## 目錄

- [專案簡介](#專案簡介)
- [核心玩法](#核心玩法)
- [系統功能](#系統功能)
- [技術與目錄](#技術與目錄)
- [快速開始](#快速開始)
- [產品截圖](#產品截圖)
- [常見問題](#常見問題)
- [相關文件](#相關文件)
- [授權與合規](#授權與合規)
- [聯絡我們](#聯絡我們)

## 專案簡介

Fishing Coin Lobby（捕魚金幣大廳 / 捕魚大廳）是一套街機捕魚遊戲平台原始碼。目前 README 描述的主要內容包括：

- 海魔來襲、經典模式、比賽模式、玉石場和「找刺激」等玩法
- 商城、個人中心、寶箱、排行榜、保險箱、好友、郵件與設定系統
- 任務、每日登入、活動中心、邀請好友、JackPot、刮刮樂和轉盤活動
- Cocos Creator 客戶端工程、服務端工具與多語言文件
- 面向 iOS 與 Android 的客戶端介面

具體功能、倍率和平台支援範圍以目前原始碼、設定與文件為準。

## 核心玩法

### 海魔來襲

BOSS 級海魔隨機登場，包含全螢幕攻擊和擊殺獎勵機制。

### 經典模式

| 場景 | 倍率範圍 | 說明 |
|---|---:|---|
| 海妖漩渦 | 1-5000 倍 | 魚群密集的入門場景 |
| 新手灘 | 1-1000 倍 | 面向新玩家的基礎場景 |
| 深海巨獸 | 1000-20000 倍 | 大型魚類場景 |
| 幽靈船長 | 5000-30000 倍 | 包含 BOSS 戰的高倍率場景 |

### 比賽模式

定時開啟捕魚比賽，玩家同場競技，並依照積分排名發放獎勵。

### 玉石場

| 場景 | 倍率範圍 | 說明 |
|---|---:|---|
| 亡靈廢墟 | 5000-8000 倍 | 暗黑風格與稀有魚種 |
| 天宮亂鬥 | 8000-10000 倍 | 包含全螢幕炸彈與連鎖閃電 |

### 找刺激

原 README 列出的休閒玩法包括彈頭奪寶、四國征戰、寶石迷城、鬥地主、麻將、拼十、王者戰績、水滸傳、好運連連、龍虎鬥與紅黑大戰。

## 系統功能

- **商城系統**：金幣、鑽石、道具、彈頭、VIP 禮包與限時折扣
- **個人中心**：頭像、暱稱、戰績、資產、等級與成就
- **寶箱系統**：不同等級寶箱與定時獎勵
- **排行榜**：日榜、週榜、月榜與多種統計維度
- **保險箱**：遊戲資產存取功能
- **好友系統**：好友、私聊、戰績查看與對戰邀請
- **郵件系統**：公告、活動獎勵、補償與客服回覆
- **Facebook 登入**：帳號登入、好友邀請與分享
- **設定中心**：音效、音樂、語言、通知與帳號設定
- **營運活動**：任務、每日登入、活動中心、邀請、獎池、刮刮樂、轉盤與激勵廣告

## 技術與目錄

| 模組 | 真實路徑 | 說明 |
|---|---|---|
| Cocos 客戶端 | `assets/` | 場景、腳本與資源中繼資料 |
| 場景 | `assets/scene/` | Cocos 場景檔案 |
| 遊戲腳本 | `assets/script/` | 客戶端邏輯腳本 |
| 服務端工具 | `server/` | 範本、Web 服務目錄與腳本 |
| 工具 | `tools/` | 設定與輔助工具 |
| 文件 | `doc/`、`docs/` | 專案文件、網頁與圖片資源 |

```text
fishing-game-source/
├── assets/
│   ├── scene/
│   └── script/
├── server/
│   ├── tpl/
│   └── webserver/
├── tools/
├── doc/
├── docs/
│   └── assets/screenshots/
├── project.json
├── jsconfig.json
└── README.md
```

## 快速開始

```bash
git clone https://github.com/alibabamayun888/fishing-game-source.git
cd fishing-game-source
```

這是一個 Cocos Creator 工程。開發前請依照 `project.json`、`creator.d.ts` 與現有資源選擇相容的 Cocos Creator 版本。客戶端內容位於 `assets/`，服務端相關說明位於 [`server/readme`](server/readme)。

> 倉庫根目錄目前沒有 Docker Compose、Kubernetes 或獨立 `Admin/` 目錄，因此本文不提供相關部署指令或預設後台帳號。

## 產品截圖

<table>
  <tr><td><img src="docs/assets/screenshots/x1.jpg" alt="Cocos 捕魚金幣大廳介面" width="380"></td><td><img src="docs/assets/screenshots/zhandou.jpg" alt="Fishing Game 捕魚戰鬥介面" width="380"></td></tr>
  <tr><td><img src="docs/assets/screenshots/hx3.jpg" alt="捕魚遊戲海魔來襲場景" width="380"></td><td><img src="docs/assets/screenshots/jx1.jpg" alt="經典街機捕魚遊戲場景" width="380"></td></tr>
  <tr><td><img src="docs/assets/screenshots/ysx1.jpg" alt="捕魚遊戲玉石場介面" width="380"></td><td><img src="docs/assets/screenshots/yu.png" alt="Fish Shooter 捕魚遊戲魚類資源" width="380"></td></tr>
</table>

更多圖片請參閱 [`docs/assets/screenshots/`](docs/assets/screenshots/)。

## 常見問題

### 可以用於商業營運嗎？

原始碼僅供學習、研究與展示。商業使用需要另行取得授權，並遵守所在地法律、平台政策與專案授權條款。

### 支援哪些客戶端平台？

原 README 標示支援 iOS 12+ 與 Android 5+。實際建置範圍取決於 Cocos Creator 版本、專案設定與第三方相依套件。

### 如何開始二次開發？

客戶端場景與腳本分別位於 `assets/scene/` 和 `assets/script/`。服務端範本與腳本位於 `server/`，輔助工具位於 `tools/`。

### 是否提供一鍵部署？

目前倉庫根目錄沒有 Compose 檔案或完整部署定義。請勿直接使用舊 README 中引用 Docker、`Admin/` 或大寫 `Server/` 的指令。

## 相關文件

- [更新記錄](CHANGELOG.md)
- [貢獻指南](CONTRIBUTING.md)
- [安全政策](SECURITY.md)
- [支援說明](SUPPORT.md)
- [負責任使用規範](RESPONSIBLE-USE.md)
- [服務端說明](server/readme)

## 授權與合規

本專案採用自訂授權條款。學習、研究、散布與商業使用條件以現有專案說明為準；商業使用需要另行取得授權。任何上線、支付、虛擬資產、廣告或應用程式商店發布行為，都必須遵守當地法律與平台規則。

## 聯絡我們

| 管道 | 聯絡方式 |
|---|---|
| Email | `ttpoker40@gmail.com` |
| Telegram | [@alibabama401](https://t.me/alibabama401) |
| GitHub Issues | [提交問題](https://github.com/alibabamayun888/fishing-game-source/issues) |

