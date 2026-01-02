```
                     _    _ _ _
                    | |  (_) | |
  _ __    ___  ___  | | ___| | |___
 | '_ \  / __|/ _ \ | |/ / | | / __|
 | | | | \__ \ (_) ||   <| | | \__ \
 |_| |_| |___/\___/ |_|\_\_|_|_|___/

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Curated Skills for AI Agents
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

<div align="center">

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![agentskills.io](https://img.shields.io/badge/format-agentskills.io-purple.svg)](https://agentskills.io)
[![AGENTS.md](https://img.shields.io/badge/discovery-AGENTS.md-green.svg)](https://www.infoq.com/news/2025/08/agents-md/)

**One marketplace. Every agent. No bullshit.**

[Install](#-quick-start) · [Skills](#-available-skills) · [Contribute](CONTRIBUTING.md) · [Philosophy](#-philosophy)

</div>

---

## 💡 Philosophy

> **"Complexity is a drag."**

Every coding agent invented their own instruction format. It's chaos:

```
Claude Code    →  CLAUDE.md, .claude/skills/
GitHub Copilot →  AGENTS.md, copilot-instructions.md, CLAUDE.md, GEMINI.md
Codex          →  SKILL.md, ~/.codex/skills/
Cursor         →  .cursorrules (deprecated), .cursor/rules/*.mdc
Windsurf       →  Cascade Rules, Memories
Cline          →  .clinerules
Factory/Droid  →  .factory/droids/*.md
Amp Code       →  Workspaces via web
Aider          →  AGENTS.md, .aider.conf.json
```

**Maintaining five hand-written cheat sheets is silly.**

### The n-skills Way

We don't fight the fragmentation. We transcend it:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   SKILL.md          →  The universal skill format      │
│   AGENTS.md         →  The universal discovery file    │
│   openskills        →  The universal installer         │
│                                                         │
│   Write once. Run everywhere.                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

[AGENTS.md](https://www.infoq.com/news/2025/08/agents-md/) is now adopted by **20,000+ repositories** and natively supported by GitHub Copilot, Google Gemini, OpenAI Codex, Factory Droid, Cursor, and more.

**n-skills is just a curated marketplace.** No CLI. No complexity. [openskills](https://github.com/numman-ali/openskills) handles everything else.

---

## 🚀 Quick Start

### Claude Code
```bash
/plugin marketplace add numman-ali/n-skills
/plugin install zai-cli@n-skills
```

### OpenSkills (Universal)
```bash
openskills install numman-ali/n-skills
```
Works with: **Cursor** · **Windsurf** · **Cline** · **Aider** · any AGENTS.md-compatible agent

### Codex
```bash
$skill-installer https://github.com/numman-ali/n-skills/tree/main/skills/tools/zai-cli
```

---

## 📦 Available Skills

| Skill | Category | Description |
|:------|:---------|:------------|
| **[zai-cli](./skills/tools/zai-cli/)** | `tools` | Z.AI vision, search, reader, and GitHub exploration via MCP |

> More skills coming soon. Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🗂️ Categories

| Category | What goes here |
|:---------|:---------------|
| `tools` | CLI tools and utilities |
| `development` | Language-specific dev assistance |
| `productivity` | Workflow automation |
| `automation` | Browser, CI/CD, system automation |
| `data` | Databases, data processing |
| `documentation` | Docs, diagrams, specs |

---

## 🌐 Universal Compatibility

n-skills works everywhere because we use open standards:

| Agent | How it works | Status |
|:------|:-------------|:------:|
| **Claude Code** | Native plugin system | ✅ Native |
| **GitHub Copilot** | Reads AGENTS.md directly | ✅ Native |
| **Codex** | $skill-installer | ✅ Native |
| **Factory/Droid** | Reads AGENTS.md directly | ✅ Native |
| **Cursor** | openskills → AGENTS.md | ✅ Universal |
| **Windsurf** | openskills → AGENTS.md | ✅ Universal |
| **Cline** | openskills → AGENTS.md | ✅ Universal |
| **Aider** | openskills → AGENTS.md | ✅ Universal |
| **Amp Code** | openskills → AGENTS.md | ✅ Universal |

---

## 📁 Repository Structure

```
n-skills/
├── .claude-plugin/
│   └── marketplace.json     # Claude Code registry
├── AGENTS.md                # Universal discovery
├── skills/
│   ├── tools/
│   │   └── zai-cli/         # Flagship skill
│   ├── development/
│   ├── productivity/
│   ├── automation/
│   ├── data/
│   └── documentation/
└── docs/
    ├── skill-format.md      # How to write skills
    ├── cross-platform.md    # Multi-agent compatibility
    └── categories.md        # Category guidelines
```

---

## 🤝 Contributing

This is a **curated** marketplace. Quality over quantity.

1. Fork this repo
2. Add your skill to the appropriate category
3. Update `marketplace.json` and `AGENTS.md`
4. Open a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## 🔗 Related Projects

- **[openskills](https://github.com/numman-ali/openskills)** — Universal skills installer for all AI agents
- **[zai-cli](https://github.com/numman-ali/zai-cli)** — Z.AI capabilities via CLI and MCP
- **[agentskills.io](https://agentskills.io)** — The open standard for AI agent skills

---

<div align="center">

**Built for developers who value simplicity.**

Apache 2.0 · Made by [@numman-ali](https://github.com/numman-ali)

</div>
