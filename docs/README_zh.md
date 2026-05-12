<div align="center">

<img src="./assets/logo.svg" alt="n-skills" width="400"/>

<br/>
<br/>

**由 [Numman Ali](https://x.com/nummanali) 精心策划**

[![Twitter Follow](https://img.shields.io/twitter/follow/nummanali?style=social)](https://x.com/nummanali)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![agentskills.io](https://img.shields.io/badge/format-agentskills.io-purple.svg)](https://agentskills.io)
[![AGENTS.md](https://img.shields.io/badge/discovery-AGENTS.md-green.svg)](https://www.infoq.com/news/2025/08/agents-md/)

**一个市场，所有智能体。**

[快速开始](#-快速开始) · [技能列表](#-可用技能) · [提交技能](#-想要上榜) · [设计理念](#-设计理念)

</div>

---

## 💡 设计理念

> **"一次编写，到处运行。"**

AI 编程智能体正在快速发展，每个智能体都有自己的工作方式：

```
Claude Code    →  CLAUDE.md, .claude/skills/
GitHub Copilot →  AGENTS.md, copilot-instructions.md
Codex          →  SKILL.md, ~/.codex/skills/
Cursor         →  .cursor/rules/*.mdc
Windsurf       →  Cascade Rules, Memories
Cline          →  .clinerules
Factory/Droid  →  .factory/droids/*.md
OpenCode       →  .opencode/skill/, opencode.json
```

### n-skills 的方式

我们以通用方式拥抱多样性：

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   SKILL.md          →  通用技能格式                      │
│   AGENTS.md         →  通用发现文件                      │
│   openskills        →  通用安装器                        │
│                                                         │
│   一次编写，到处运行。                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

[AGENTS.md](https://www.infoq.com/news/2025/08/agents-md/) 已被 **20,000+ 个仓库** 采用，并获得 GitHub Copilot、Google Gemini、OpenAI Codex、Factory Droid、Cursor 等原生支持。

**n-skills 是一个精选市场。** 通过 [openskills](https://github.com/numman-ali/openskills) 安装，或使用智能体的原生安装器——由你选择！

---

## 🚀 快速开始

### Claude Code

```bash
/plugin marketplace add numman-ali/n-skills
```

然后安装任意技能：
```bash
/plugin install orchestration@n-skills
/plugin install open-source-maintainer@n-skills
/plugin install gastown@n-skills
/plugin install dev-browser@n-skills
/plugin install zai-cli@n-skills
```

### OpenSkills（通用方式）

适用于 **所有智能体**：Claude Code、Cursor、Windsurf、Cline、OpenCode，以及任何读取 AGENTS.md 的工具。

```bash
npm i -g openskills
openskills install numman-ali/n-skills
openskills sync
```

> **初次接触 OpenSkills？** 它是通用技能安装器。[了解更多 →](https://github.com/numman-ali/openskills)

<details>
<summary><strong>其他原生安装器</strong></summary>

**Codex：**
```bash
$skill-installer https://github.com/numman-ali/n-skills/tree/main/skills/tools/zai-cli
```

</details>

---

## 📦 可用技能

| 技能 | 分类 | 来源 | 描述 |
|:------|:---------|:-------|:------------|
| **[orchestration](./skills/workflow/orchestration/)** | `workflow` | 原生 | 基于 cc-mirror 任务和 TodoWrite 的多智能体编排 |
| **[open-source-maintainer](./skills/workflow/open-source-maintainer/)** | `workflow` | 原生 | 开源项目的端到端 GitHub 仓库维护 |
| **[dev-browser](./skills/automation/dev-browser/)** | `automation` | [SawyerHood](https://github.com/SawyerHood/dev-browser) | 带持久页面状态的浏览器自动化 |
| **[gastown](./skills/tools/gastown/)** | `tools` | 原生 | 多智能体编排器（配合 Claude Code + Opus 效果最佳） |
| **[zai-cli](./skills/tools/zai-cli/)** | `tools` | 原生 | 通过 MCP 实现 Z.AI 视觉、搜索、阅读器和 GitHub 探索 |

> 更多技能即将推出。想贡献？请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🗂️ 分类

| 分类 | 包含内容 |
|:---------|:---------------|
| `workflow` | 多智能体编排、任务协调 |
| `tools` | CLI 工具和实用程序 |
| `development` | 特定语言的开发辅助 |
| `productivity` | 工作流自动化 |
| `automation` | 浏览器、CI/CD、系统自动化 |
| `data` | 数据库、数据处理 |
| `documentation` | 文档、图表、规范 |

---

## 🎯 想要上榜？

这是一个 **精选** 市场。任何人都可以申请加入，但只有 **高质量、真正有价值的项目** 才会被考虑。

**我们关注的：**
- 解决实际问题的技能
- 清晰、文档完善的代码
- 对开发者有真正帮助
- 积极维护

**不感兴趣的：**
- 没有实际价值的包装型技能
- 已弃用或缺乏维护的项目
- 低质量的提交

### 如何提交

1. 提交一个 [issue](https://github.com/numman-ali/n-skills/issues)，说明你的技能详情
2. 解释它的功能和价值
3. 审核通过后，按照 [CONTRIBUTING.md](CONTRIBUTING.md) 提交 PR

或在 X 上私信我：[@nummanali](https://x.com/nummanali)

---

## 🌐 通用兼容性

n-skills 可在任何地方使用，因为我们采用开放标准：

| 智能体 | 工作方式 | 状态 |
|:------|:-------------|:------:|
| **Claude Code** | 原生插件系统 | ✅ 原生 |
| **GitHub Copilot** | 直接读取 AGENTS.md | ✅ 原生 |
| **Codex** | $skill-installer | ✅ 原生 |
| **Factory/Droid** | 直接读取 AGENTS.md | ✅ 原生 |
| **Cursor** | openskills → AGENTS.md | ✅ 通用 |
| **Windsurf** | openskills → AGENTS.md | ✅ 通用 |
| **Cline** | openskills → AGENTS.md | ✅ 通用 |
| **OpenCode** | 原生技能支持 | ✅ 原生 |
| **Amp Code** | openskills → AGENTS.md | ✅ 通用 |

---

## 🔄 上游自动同步

外部技能会自动与源仓库保持同步。

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   你的仓库                 n-skills                          │
│   ────────                 ────────                         │
│   skills/my-skill/     →  skills/category/my-skill/        │
│                                                             │
│   每日定时同步你的最新更改。                                  │
│   你保留所有权。我们负责策展。                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**工作原理：**
1. 你在自己的仓库中维护技能
2. 通过 PR 添加条目到 [`sources.yaml`](sources.yaml)
3. GitHub Actions 每日同步你的技能文件夹
4. 通过 `.source.json` 保留归属信息

**为什么不用子模块？** 子模块地狱是真实存在的。这种方式更简单，可与 openskills、Claude Code 和其他所有工具无缝配合，无需特殊处理。

---

## 📁 仓库结构

```
n-skills/
├── .claude-plugin/
│   └── marketplace.json       # Claude Code 注册表
├── .github/workflows/
│   └── sync-skills.yml        # 每日同步自动化
├── scripts/
│   ├── sync-external.mjs      # 同步引擎
│   └── update-registry.mjs    # 注册表生成器
├── sources.yaml               # 外部技能清单
├── AGENTS.md                  # 通用发现文件
├── skills/
│   ├── automation/
│   │   └── dev-browser/              # 从 SawyerHood 同步
│   │       ├── .claude-plugin/
│   │       └── skills/dev-browser/   # SKILL.md 在这里
│   ├── tools/
│   │   ├── gastown/
│   │   │   ├── .claude-plugin/
│   │   │   └── skills/gastown/
│   │   └── zai-cli/
│   │       ├── .claude-plugin/
│   │       └── skills/zai-cli/
│   └── workflow/
│       ├── orchestration/
│       │   ├── .claude-plugin/
│       │   └── skills/orchestration/
│       └── open-source-maintainer/
│           ├── .claude-plugin/
│           └── skills/open-source-maintainer/
└── docs/
    ├── skill-format.md        # 如何编写技能
    ├── cross-platform.md      # 多智能体兼容性
    └── categories.md          # 分类指南
```

---

## 🔗 相关项目

- **[openskills](https://github.com/numman-ali/openskills)** — 适用于所有 AI 智能体的通用技能安装器
- **[zai-cli](https://github.com/numman-ali/zai-cli)** — 通过 CLI 和 MCP 实现 Z.AI 功能
- **[agentskills.io](https://agentskills.io)** — AI 智能体技能的开放标准

---

<div align="center">

**为追求简洁的开发者而建。**

Apache 2.0 · 由 [@numman-ali](https://github.com/numman-ali) 制作

</div>
