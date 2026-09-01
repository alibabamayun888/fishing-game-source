# Fishing Game Source Code｜Cocos Fish Shooter and Coin Lobby

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

<p align="center">
  <img src="https://img.shields.io/badge/Client-Cocos%20Creator-blue?style=flat-square" alt="Cocos Creator fishing game client">
  <img src="https://img.shields.io/badge/Language-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript game scripts">
  <img src="https://img.shields.io/badge/Platform-iOS%20%7C%20Android-blueviolet?style=flat-square" alt="iOS and Android fishing game">
</p>

**Fishing Game Source** is a Cocos fish-shooter source-code project featuring a fishing coin lobby, classic stages, tournaments, a jade room, boss encounters, casual mini-games, and supporting platform modules. The repository includes client assets and scripts, server tools, documentation, and product screenshots.

## Contents

- [Overview](#overview)
- [Game Modes](#game-modes)
- [Platform Features](#platform-features)
- [Technology and Layout](#technology-and-layout)
- [Getting Started](#getting-started)
- [Screenshots](#screenshots)
- [FAQ](#faq)
- [Documentation](#documentation)
- [License and Compliance](#license-and-compliance)
- [Contact](#contact)

## Overview

Fishing Coin Lobby is an arcade fishing game source-code project. The current README describes:

- Sea Monster Attack, Classic Mode, Tournament Mode, Jade Room, and casual modes
- Shop, profile, chests, leaderboards, safe box, friends, mail, and settings
- Tasks, daily login, activities, invitations, jackpot, scratch cards, and prize wheel
- A Cocos Creator client project, server tools, and multilingual documentation
- Client interfaces intended for iOS and Android

The exact feature set, reward multipliers, and platform support depend on the current source code, configuration, and documentation.

## Game Modes

### Sea Monster Attack

A boss encounter featuring full-screen attacks and defeat rewards.

### Classic Mode

| Stage | Multiplier Range | Description |
|---|---:|---|
| Siren Whirlpool | 1-5000x | Entry-level stage with dense fish groups |
| Beginner Beach | 1-1000x | Basic stage for new players |
| Deep-Sea Beast | 1000-20000x | Stage featuring large fish |
| Ghost Captain | 5000-30000x | High-multiplier boss stage |

### Tournament Mode

Scheduled fishing tournaments rank players by points and distribute rewards accordingly.

### Jade Room

| Stage | Multiplier Range | Description |
|---|---:|---|
| Undead Ruins | 5000-8000x | Dark-themed stage with rare fish |
| Celestial Battle | 8000-10000x | Includes full-screen bombs and chain lightning |

### Casual Modes

The original README lists mini-games including Bullet Treasure, Four Nations, Gem Maze, Dou Dizhu, Mahjong, Ten Cards, Battle Records, Water Margin, Lucky Streak, Dragon Tiger, and Red vs. Black.

## Platform Features

- **Shop:** coins, diamonds, items, bullets, VIP packages, and limited offers
- **Profile:** avatar, nickname, records, assets, levels, and achievements
- **Chests:** multiple chest levels and timed rewards
- **Leaderboards:** daily, weekly, monthly, and category rankings
- **Safe Box:** in-game asset storage
- **Friends:** private chat, records, and game invitations
- **Mail:** announcements, rewards, compensation, and support replies
- **Facebook Login:** sign-in, invitations, and sharing
- **Settings:** sound, music, language, notifications, and account options
- **Operations:** tasks, daily login, activity center, invitations, jackpot, scratch cards, wheel, and rewarded ads

## Technology and Layout

| Module | Repository Path | Description |
|---|---|---|
| Cocos Client | `assets/` | Scenes, scripts, and resource metadata |
| Scenes | `assets/scene/` | Cocos scene files |
| Game Scripts | `assets/script/` | Client logic scripts |
| Server Tools | `server/` | Templates, web-server directory, and scripts |
| Tools | `tools/` | Configuration and helper tools |
| Documentation | `doc/`, `docs/` | Project documents, web pages, and images |

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

## Getting Started

```bash
git clone https://github.com/alibabamayun888/fishing-game-source.git
cd fishing-game-source
```

This is a Cocos Creator project. Select a compatible editor version based on `project.json`, `creator.d.ts`, and the checked-in assets. Client content is under `assets/`; server-related notes are available in [`server/readme`](server/readme).

> The repository root currently does not include Docker Compose, Kubernetes, or a standalone `Admin/` application. This README therefore does not provide deployment commands or default admin credentials for those components.

## Screenshots

<table>
  <tr><td><img src="docs/assets/screenshots/x1.jpg" alt="Cocos fishing coin lobby screen" width="380"></td><td><img src="docs/assets/screenshots/zhandou.jpg" alt="Fishing Game battle screen" width="380"></td></tr>
  <tr><td><img src="docs/assets/screenshots/hx3.jpg" alt="Sea Monster Attack fishing stage" width="380"></td><td><img src="docs/assets/screenshots/jx1.jpg" alt="Classic arcade fish-shooter stage" width="380"></td></tr>
  <tr><td><img src="docs/assets/screenshots/ysx1.jpg" alt="Fishing game jade room" width="380"></td><td><img src="docs/assets/screenshots/yu.png" alt="Fish Shooter game fish asset" width="380"></td></tr>
</table>

More images are available under [`docs/assets/screenshots/`](docs/assets/screenshots/).

## FAQ

### Can this project be used commercially?

The source is provided for learning, research, and demonstration. Commercial use requires separate authorization and compliance with local laws, platform policies, and the project license.

### Which client platforms are supported?

The original README identifies iOS 12+ and Android 5+. Actual build support depends on the Cocos Creator version, project settings, and third-party dependencies.

### Where should secondary development begin?

Client scenes and scripts are under `assets/scene/` and `assets/script/`. Server templates and scripts are under `server/`, while helper tools are under `tools/`.

### Is one-click deployment included?

The repository root currently has no Compose file or complete deployment definition. Do not use the old README commands that reference Docker, `Admin/`, or uppercase `Server/` paths.

## Documentation

- [Changelog](CHANGELOG.md)
- [Contribution Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Support](SUPPORT.md)
- [Responsible Use](RESPONSIBLE-USE.md)
- [Server Notes](server/readme)

## License and Compliance

This project uses a custom license. Refer to the current project terms for learning, research, distribution, and commercial-use conditions. Commercial use requires separate authorization. Any launch, payment, virtual-asset, advertising, or app-store activity must comply with local laws and platform rules.

## Contact

| Channel | Contact |
|---|---|
| Email | `ttpoker40@gmail.com` |
| Telegram | [@alibabama401](https://t.me/alibabama401) |
| GitHub Issues | [Open an issue](https://github.com/alibabamayun888/fishing-game-source/issues) |


