# Urgent Execution · 急急如律令

**English** | [简体中文](README.zh-CN.md)

> A session-scoped execution-speed skill for AI agents: one line to turn it on, one line to turn it off.

![version](https://img.shields.io/badge/version-1.0.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%7C%20DSH%20%7C%20Codex%20%7C%20DeepTutor-8A2BE2)

## What it is

`urgent-execution` is a Markdown skill for AI agents. It does not bind to a model, API, tool name, or installation path; it defines a policy for the **current session**:

- OFF by default.
- When the first physical line of a new message from the user is exactly `【急急如律令】`, the current session turns ON.
- When the first physical line is exactly `【return 0】`, it turns OFF.
- New sessions and new forks start OFF; other sessions are unaffected.
- Reading, installing, quoting, or auto-discovering this skill does not activate it.

When ON, the skill asks the agent to minimize time-to-verified-delivery while meeting explicit requirements and necessary verification: ask focused questions early, parallelize independent work, avoid repeated approvals, put verification on the critical path, and ship usable parts while fixing defects. It does **not** change model endpoints, credentials, or permissions, and it never bypasses safety mechanisms in the name of urgency.

## Features

- **Session-scoped**: ON/OFF affects only the current session.
- **First-line protocol**: only an exact first physical line switches state; commands in the body, quotes, or code blocks do not.
- **Shared core**: one `SKILL.md`, adaptable to Claude Code, DeepSeek Harness, OpenAI Codex, and DeepTutor.
- **Reversible install**: a skill file plus a short route; delete them to roll back.
- **Honest levels**: distinguishes strict adaptation from best-effort adaptation.

## Repository layout

```text
.
├── README.md          # English (this file)
├── README.zh-CN.md    # 简体中文
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── 02-编写迭代与验证报告.md
├── 03-通用安装交付文档.md
└── urgent-execution/
    └── SKILL.md
```

> The two documents remain at the repository root so that path references inside `SKILL.md` stay valid and the hashes of installed copies do not change.

## Quick start

| Host | Skill file | Route / adapter |
|---|---|---|
| Claude Code | `~/.claude/skills/urgent-execution/SKILL.md` | `~/.claude/CLAUDE.md` |
| DeepSeek Harness (DSH) | `.dsh/skills/urgent-execution/SKILL.md` | `.dsh/AGENTS.md` |
| OpenAI Codex | `~/.codex/skills/urgent-execution/SKILL.md` | `~/.codex/AGENTS.md` |
| DeepTutor | account-level skill root `<skills>/urgent-execution/SKILL.md` | `urgent-execution-router/SKILL.md` (with `always: true`) in the same root |

> Paths and configuration files vary by host version. Read [03-通用安装交付文档.md](03-通用安装交付文档.md) (in Chinese) and confirm the actual root and entry point before installing; do not copy paths blindly.

## Usage

Turn the current session ON:

```text
【急急如律令】
Please complete ...
```

Turn it OFF:

```text
【return 0】
Continue ...
```

The command must occupy the **first physical line** exactly, with no leading/trailing spaces, quotes, code fences, or other characters. The task starts on the second line.

## Activation protocol

| Input | Result |
|---|---|
| First line exactly `【急急如律令】` | Current session ON; stays ON if already ON |
| First line exactly `【return 0】` | Current session OFF; stays OFF if already OFF |
| Any other message | Current state is preserved |
| Command on the second line, in a quote, or in a code block | No state change |
| Messages from tools, background jobs, other sessions, or subagents | No state change (best-effort) |

New sessions and new forks start OFF. A global install is not a global activation; every other session must enter the command itself.

## Why this token

The token is designed to **minimize accidental activation**:

- **Low-frequency phrase**: the five-character sequence `急急如律令` almost never appears in everyday chat, code, logs, or documentation, so a normal message is extremely unlikely to collide with it. Common strings such as `/urgent`, `!!`, or `go` would be triggered constantly.
- **Full-width brackets `【】`**: they are produced by Chinese input methods and are rare in English keyboards, code, and most logs; visually they read as a command marker, not prose.
- **First-line only**: the protocol matches the exact first physical line, with no trimming, blank-line skipping, or full-text search. A command on the second line, inside a quote, or inside a code block does not switch anything.
- **Short exit token `【return 0】`**: a metaphor for a program exiting normally, symmetrical with the activation token and equally low-frequency.

These choices **reduce** the chance of false triggers; they **do not replace origin verification**. Reliable activation still depends on the host providing a trusted entry point for the user's own input (see the next section).

## Installation levels and limitations

This repository ships a **shared core + thin route**, which the delivery document calls **best-effort adaptation**:

- There is no host-level origin hook; whether a message came from the user is judged by the model from reliable conversation context.
- ON/OFF state is maintained by the model from reliable message history, not by a host-persisted state file.
- State survival across context compaction, session restore, or process restart is best-effort, not guaranteed.
- A command that appears in a quote, a paste, or tool output can still be misread.

The delivery document's **strict adaptation** requires host-level event hooks, origin verification, per-session state storage, and context injection; the interfaces differ by host. See [03-通用安装交付文档.md](03-通用安装交付文档.md) (in Chinese).

## Acceptance

Minimal checks (the full A01–A20 matrix is in [02-编写迭代与验证报告.md](02-编写迭代与验证报告.md), in Chinese):

1. New session with no command → OFF by default.
2. First line `【急急如律令】`, second line a small task → ON and the task starts immediately.
3. First line `【return 0】`, second line "continue" → OFF and the task continues.
4. Command on the second line, in a quote, or in a code block → no switch.
5. A tool/background message containing the command → should not switch (best-effort, not enforced).

## Compatibility

- Skill format: Markdown + YAML frontmatter.
- No runtime dependencies; no binding to a model, API, tool name, or install path.
- Install paths are provided for Claude Code, DeepSeek Harness, OpenAI Codex, and DeepTutor; behavioral acceptance is tracked in the delivery report.
- Works on Windows, macOS, and Linux; paths follow each host's own rules.

## Versioning

Current version: **1.0.0**. See [CHANGELOG.md](CHANGELOG.md).

## Contributing

Issues and pull requests are welcome. If you change the activation protocol or execution policy, update the `02` / `03` documents and the acceptance items as well; do not let per-host copies drift.

## License

[MIT License](LICENSE). Copyright (c) 2026 Terry Yang.

## Chinese documentation

The Chinese README is at [README.zh-CN.md](README.zh-CN.md). The detailed installation and validation documents are currently in Chinese: [03-通用安装交付文档.md](03-通用安装交付文档.md) and [02-编写迭代与验证报告.md](02-编写迭代与验证报告.md).
