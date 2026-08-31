[簡體中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# fishing-game-source｜捕鱼遊戲源碼 | Fishing Game Source Code | Cocos+C++ 街机捕鱼平台 | 經典模式+比賽+玉石場

<p align="center">
  <img src="https://img.shields.io/badge/Cocos2d-x-3.17+-blue?style=for-the-badge" alt="Cocos">
  <img src="https://img.shields.io/badge/C%2B%2B-17-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++17">
  <img src="https://img.shields.io/badge/Node.js-18+-brightgreen?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL 8.0">

 <img src="https://img.shields.io/badge/iOS%20%7C%20Android-Cross%20Platform-blueviolet?style=for-the-badge" alt="Cross Platform">
</p>

<h1 align="center">🎣 Fishing Coin Lobby</h1>

<p align="center">
  <b>捕鱼金币大厅源碼 / 捕鱼积分大厅源碼 — 商业级街机遊戲平台</b><br>
  <b>Commercial Fishing Coin Lobby Source Code | Arcade Game Platform</b><br>
  <b>支持 iOS / Android | 海魔来袭+經典模式+比賽+玉石場+找刺激 | 快速二次開發</b>
</p>
<p align="center">
  <a href="#核心玩法">🎮 核心玩法</a> •
  <a href="#系統功能">🛒 系統功能</a> •
  <a href="#技術架構">⚙️ 技術架構</a> •
  <a href="#部署指南">🚀 快速部署</a>
</p>

---

## 閱讀與下載

- 建議先閱讀本 README，了解玩法、功能模块、技術架構、部署與二次開發范围。
- 產品截圖统一讀取 `docs/assets/screenshots/` 目錄下的真實文件；上传时请保持目錄名和文件名大小写完全一致。
- 如需评估源碼、演示包、部署或二次開發，请通過文末 Email 或 Telegram 聯系。

## 產品截圖

以下截圖直接讀取仓庫 `docs/assets/screenshots/` 目錄下的產品圖片。

![捕鱼遊戲產品截圖 01](docs/assets/screenshots/dx3.jpg)
![捕鱼遊戲產品截圖 02](docs/assets/screenshots/hx3.jpg)
![捕鱼遊戲產品截圖 03](docs/assets/screenshots/jx1.jpg)
![捕鱼遊戲產品截圖 04](docs/assets/screenshots/jx4.jpg)
![捕鱼遊戲產品截圖 05](docs/assets/screenshots/nx1.jpg)
![捕鱼遊戲產品截圖 06](docs/assets/screenshots/x1.jpg)
![捕鱼遊戲產品截圖 07](docs/assets/screenshots/x1s.jpg)
![捕鱼遊戲產品截圖 08](docs/assets/screenshots/x2.jpg)
![捕鱼遊戲產品截圖 09](docs/assets/screenshots/ysx1.jpg)
![捕鱼遊戲產品截圖 10](docs/assets/screenshots/yu.png)
![捕鱼遊戲產品截圖 11](docs/assets/screenshots/zhandou.jpg)

## 目錄

- [項目簡介](#項目簡介)
- [核心玩法](#核心玩法)
- [系統功能](#系統功能)
- [技術架構](#技術架構)
- [多語言支持](#多語言支持)
- [發佈支持](#發佈支持)
- [快速定制](#快速定制)
- [項目结構](#項目结構)
- [部署指南](#部署指南)
- [常见问题](#常见问题)
- [SEO关键词](#seo关键词)
- [许可证](#许可证)
- [聯系我们](#聯系我们)

---

## 項目簡介

**Fishing Coin Lobby（捕鱼金币大厅 / 捕鱼大厅）** 是一套完整的**商业级街机遊戲平台源碼**，专为追求高性能和稳定運行的運營商打造。

本系统包含 **海魔来袭、經典模式、比賽模式、玉石場、找刺激** 等核心玩法，覆盖 1-30000 倍率区间，内置 **商城、排行榜、保险箱、任務、JackPot、刮刮乐、轉盤** 等完整系统，以及 **Node.js 運營後台**，支持**中文、英文等多語言**，可快速打包發佈到 **iOS App Store** 和 **Google Play**。

&gt; **适合搜索关键词**：捕鱼金币大厅源碼、捕鱼积分大厅源碼、Fishing Game Source Code、Ocean King Source Code、Fish Shooter Platform、街机遊戲源碼、Arcade Game Source Code、Cocos 捕鱼源碼、C++ 街机服務器、捕鱼運營後台、捕鱼遊戲 APP 源碼、金币場捕鱼源碼、积分場捕鱼源碼、捕鱼二次開發、捕鱼定制開發、捕鱼出海、海魔来袭源碼、捕鱼比賽模式、捕鱼玉石場

| 語言 | 項目名稱 |
|------|---------|
| 中文 | 捕鱼金币大厅源碼 / 捕鱼源碼 / 街机遊戲項目 |
| English | Fishing Coin Lobby Source Code / Fish Shooter Platform |
| Tiếng Việt | Mã nguồn Sảnh Bắn Cá / Nền tảng game bắn cá |

---

## 核心玩法

### 一、海魔来袭
BOSS 级海魔随机登場，全屏攻击，击杀可获得巨額獎勵，最高可达 **30000 倍**。

### 二、經典模式
包含 4 大經典場景，倍率覆盖 1-30000 倍：

| 場景 | 倍率范围 | 特点 |
|------|---------|------|
| 海妖漩涡 | 1-5000 倍 | 新手友好，鱼群密集，易上手 |
| 新手滩 | 1-1000 倍 | 入门级場景，适合新玩家练手 |
| 深海巨兽 | 1000-20000 倍 | 大型鱼类出没，獎勵丰厚 |
| 幽灵船长 | 5000-30000 倍 | 高难度場景，BOSS 战刺激 |

### 三、比賽模式
定时開启捕鱼比賽，玩家同場竞技，按积分排名發放獎勵。

### 四、玉石場
高倍率 VIP 专属場景，倍率 5000-10000 倍：

| 場景 | 倍率范围 | 特点 |
|------|---------|------|
| 亡灵废墟 | 5000-8000 倍 | 暗黑风格，稀有鱼种 |
| 天宫乱斗 | 8000-10000 倍 | 顶级場景，全屏炸弹、连锁闪电 |

### 五、找刺激
内置 12 款休闲小遊戲，丰富玩家體验：

- 弹头夺宝
- 四国征战
- 宝石迷城
- 斗地主
- 麻将
- 拼十
- 王者战绩
- 水浒传
- 好運连连
- 龙虎斗
- 红黑大战

---

## 系統功能

### 核心系统模块

- 商城系统 — 金币/钻石获取、道具购买、弹头、VIP 礼包、限时折扣
- 个人中心 — 头像、昵稱、战绩、资產、等级、成就系统
- 宝箱系统 — 青铜/白银/黄金/钻石宝箱，定时開启獎勵
- 排行榜 — 日榜/周榜/月榜/总榜，财富榜/击杀榜/倍率榜
- 保险箱 — 金币存入保险，防止大額损失，提升留存
- 好友系统 — 添加好友、私聊、查看好友战绩、邀请对战
- 郵件系统 — 系统公告、活动獎勵、补偿發放、客服回复
- Facebook 登錄 — FB 一键登錄、好友邀请、战绩分享
- 设置中心 — 音效、音乐、語言切换、通知管理、账号安全

### 運營活动模块

- 任務系统 — 每日/每周/成长任務，完成任務领金币
- 每日登錄 — 连续登錄獎勵，第 7 天大獎
- 活动中心 — 限时活动聚合頁，节日专题活动
- 邀请好友 — 邀请碼裂变，双方得金币獎勵
- JackPot 獎池 — 全局累积獎池，随机触發大獎
- 刮刮乐彩票 — 虚拟刮刮卡，即时開獎
- 轉盤活动 — 幸運大轉盤，免费/付费抽獎
- 免费看广告 — 观看激勵视频广告得金币

---

## 技術架構

| 层级 | 技術 | 说明 |
|------|------|------|
| 客户端 | Cocos2d-x 3.17+ / Cocos Creator | 跨平台支持 iOS / Android / H5，高性能渲染 |
| 遊戲服務端 | C++17 / Boost.Asio | 高性能遊戲逻辑服務器，单节点 10000+ 并發 |
| 運營後台 | Node.js + Express + Vue3 | 完整的運營管理系统，數據可视化 |
| 數據庫 | MySQL 8.0 + Redis 7.0 | 主从复制 + 集群缓存，支撑高并發讀写 |
| 网絡协議 | WebSocket + Protobuf | 低延迟實时通信，平均延迟 &lt; 50ms |
| 消息队列 | RabbitMQ | 异步任務、削峰填谷、日志处理 |
| 部署 | Docker + Kubernetes | 容器化部署，一键扩缩容 |
| 监控 | Prometheus + Grafana | 實时性能监控、告警、運營數據看板 |

---

## 多語言支持

- 簡體中文 — 完整本地化
- English — 全球化出海标配
- Tiếng Việt — 东南亚热门市場（越南捕鱼市場巨大）
- ภาษาไทย — 泰国街机热门市場
- Bahasa Indonesia — 印尼新兴市場

&gt; 語言包采用 JSON 配置化设计，新增語言仅需翻译文件，无需改代碼。



## 快速定制

本項目采用模块化架構设计，二次開發效率极高：

| 模块 | 替换方式 | 预计工时 |
|------|---------|---------|
| UI 界面 | 替换 Cocos 場景和 UI 资源 | 1-3 天 |
| 鱼类/炮台 | 替换 Spine 动画和 Sprite 资源 | 2-4 小时 |
| 音效音乐 | 替换 Audio 资源 | 2-4 小时 |
| 遊戲名稱/Logo | 修改配置表 + 替换启动圖 | 2-4 小时 |
| 金币档位 | 修改後台配置表 | 30 分钟 |
| 活动獎勵 | 修改後台運營配置 | 30 分钟 |
| 新增語言 | 翻译 JSON 語言包 | 1-2 天 |

### 定制示例：修改遊戲名稱

```bash
# 1. 修改客户端配置
vim Client/resources/config/game.json
# 修改 "gameName": "你的遊戲名"

# 2. 修改服務端配置
vim Server/config/game.conf
# 修改 game_name = "你的遊戲名"

# 3. 修改運營後台配置
vim Admin/.env
# 修改 APP_NAME=你的遊戲名

# 4. 重新打包
./build.sh
```

## 項目结構
fishing-coin-lobby/
├── Client/                    # Cocos 客户端
│   ├── resources/             # 場景、UI、鱼类、炮台资源
│   ├── src/                   # C++ / JavaScript 遊戲逻辑
│   ├── frameworks/            # Cocos2d-x 框架
│   └── build/                 # iOS / Android 打包脚本
├── Server/                    # C++ 遊戲服務端
│   ├── Core/                  # 核心遊戲引擎（發炮、碰撞、结算）
│   ├── Network/               # 网絡层（WebSocket / TCP）
│   ├── DB/                    # 數據庫 ORM 與缓存
│   ├── Room/                  # 房间管理（經典/比賽/玉石場）
│   ├── Fish/                  # 鱼类生成與 AI 路徑
│   └── Gateway/               # 网关與负載均衡
├── Admin/                     # Node.js 運營後台
│   ├── server/                # Express 後端 API
│   ├── web/                   # Vue3 管理後台
│   └── config/                # 配置文件
├── Proto/                     # Protobuf 通信协議
├── Config/                    # 遊戲配置（倍率、鱼群、活动）
├── Docker/                    # Docker 镜像與编排
├── Docs/                      # 部署文档、API 文档、發佈指南
├── Tests/                     # 单元测试與压测脚本
└── README.md                  # 本文件



### 部署指南

环境要求

OS: Ubuntu 20.04+ / CentOS 8+
Compiler: GCC 9.4+ / Clang 12+
Build: CMake 3.20+
DB: MySQL 8.0+ / Redis 6.0+
Node.js: 18+ / npm 9+
Client: Cocos2d-x 3.17+ 或 Cocos Creator 3.x


###Docker 一键部署（推荐）
# 1. 克隆仓庫
git clone https://github.com/alibabamayun888/fishing-coin-lobby.git
cd fishing-coin-lobby

# 2. 启动全部服務（服務端 + 數據庫 + 運營後台）
docker-compose up -d

# 3. 检查服務状态
docker-compose ps

# 4. 查看遊戲服務端日志
docker-compose logs -f gameserver

# 5. 访问運營後台
open http://localhost:3000/admin
# 默认账号: admin / admin123

###手动编译部署

# 编译遊戲服務端
cd Server
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# 编译運營後台
cd ../Admin
npm install
npm run build

# 启动服務
./Server/build/GameServer --config=../Config/server.conf
cd Admin && npm start


## 聯系我们
| 渠道       | 聯系方式                                                                          |
| -------- | ----------------------------------------------------------------------------- |
| Email    | <ttpoker40@gmail.com>                                                         |
| Telegram | [@alibabama401](https://t.me/alibabama401)                                    |
| Issues   | [GitHub Issues](https://github.com/alibabamayun888/fishing-coin-lobby/issues) |


## 常见问题

Q1: 这个項目可以商用吗？需要授权吗？
A: 源碼仅供学习研究。如需商用上线運營，请聯系获取商业授权协議和技術支持。
Q2: 支持哪些平台？可以發佈到 App Store 吗？
A: 支持 iOS 12+ 和 Android 5+，已针对 App Store 和 Google Play 审核要求優化，最快 3 天可提交审核。
Q3: 二次開發难度大吗？需要多少人团队？
A: 模块化设计，UI/音效/配置均可快速替换。最小团队 1 名 Cocos 開發 + 1 名服務端開發即可在 2 周内完成定制開發上线。
Q4: 最大支持多少人在线？
A: 单节点部署支持 10000 并發，通過 K8s 横向扩展可支撑百万级 DAU。

## SEO 关键词索引

以下关键词用于搜索引擎索引，覆盖全球多語言搜索場景
## 中文关键词： 捕鱼遊戲源碼、街机遊戲源碼、Cocos 捕鱼源碼、C++ 街机服務器、捕鱼運營後台、捕鱼遊戲 APP 源碼、金币場捕鱼源碼、积分場捕鱼源碼、捕鱼二次開發、捕鱼定制開發、捕鱼出海、海魔来袭源碼、捕鱼比賽模式、捕鱼玉石場、街机捕鱼平台、Ocean King 源碼、Fish Shooter 源碼、捕鱼弹头夺宝、捕鱼四国征战、捕鱼斗地主、捕鱼麻将、捕鱼龙虎斗、捕鱼红黑大战、捕鱼水浒传、捕鱼好運连连、捕鱼遊戲引擎、捕鱼服務端源碼、街机遊戲開發、多人捕鱼遊戲、實时捕鱼服務器、捕鱼遊戲框架、捕鱼遊戲平台、捕鱼遊戲系统、捕鱼遊戲解决方案、捕鱼遊戲技術架構、捕鱼遊戲客户端、捕鱼遊戲服務端
## English Keywords: Fishing Game Source Code, Fish Shooter Platform Source Code, Ocean King Source Code, Arcade Fishing Game Source Code, Cocos Fishing Game, C++ Arcade Server, High Performance Fishing Platform, Casino Fishing Game, Fish Game App Source Code, Fishing Game for iOS, Fishing Game for Android, Fishing Game White Label, Fishing Game Custom Development, Fish Game Admin Panel, Fish Game Operation System, Fish Game Store System, Fish Game Daily Bonus, Fish Game Jackpot, Fish Game Tournament, Fish Game Jade Room, Fish Game Adventure Mode, Sea Monster Attack Fishing, Fish Shooter Coin Lobby, Fish Game Backend Node.js, Fishing Game Engine, Multiplayer Fishing Game, Real-time Fishing Server, Fishing Game Framework, Fishing Game Platform, Fishing Game System, Fishing Game Solution, Fishing Game Architecture, Fishing Game Client, Fishing Game Server, Online Fishing Game, HTML5 Fishing Game, Web Fishing Game, Mobile Fishing Game, Fishing Game Development, Fishing Game GitHub, Open Source Fishing Game, Fishing Game Demo, Fishing Game Tutorial
<p align="center">
  <b>如果这个項目对你有帮助，请点个 Star 支持一下！</b><br>
  <i>If this project helps you, please give it a star and share it with your friends!</i><br><br>
  <a href="https://github.com/alibabamayun888/fishing-coin-lobby/stargazers">
    <img src="https://img.shields.io/github/stars/alibabamayun888/fishing-coin-lobby?style=social" alt="Give a Star">
  </a>
</p>
```
