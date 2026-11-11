# 急急如律令 · urgent-execution

> 给 AI Agent 的会话级执行加速技能：一行开启，一行退出；只作用于当前会话。

![version](https://img.shields.io/badge/version-1.0.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%7C%20DSH%20%7C%20Codex%20%7C%20DeepTutor-8A2BE2)

## 这是什么

`urgent-execution` 是一份面向 AI Agent 的 Markdown 技能。它不绑定模型、API、工具名称或安装路径，只定义一套**当前会话**的执行策略：

- 默认 OFF；
- 用户本人新消息的第一物理行精确为 `【急急如律令】` 时，当前会话进入 ON；
- 第一物理行精确为 `【return 0】` 时，退出 ON；
- 新会话、新分叉默认 OFF；其他会话不受影响；
- 阅读、安装、引用或自动发现本技能，都不构成激活。

ON 时，技能要求 Agent 在满足显性需求和必要验证的前提下，尽量缩短“需求 → 可验收交付”的总时间：需求不清立即集中追问、主动并行、减少重复请示、把验证放进关键路径、发现问题时并行修复与交付。它**不改变**模型 endpoint、凭据、权限，也不会因为“紧急”绕过安全机制。

## 特性

- **会话隔离**：ON/OFF 只作用于当前会话，不污染其他会话。
- **首行协议**：只认第一物理行的精确口令；正文、引用、代码块里的口令不生效。
- **通用核心**：一份 `SKILL.md`，可适配 Claude Code、DeepSeek Harness、OpenAI Codex、DeepTutor。
- **安装可回滚**：技能文件 + 短路由，删除即恢复。
- **诚实分级**：区分“可靠适配”和“尽力适配”，不虚报严格触发。

## 目录结构

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── 02-编写迭代与验证报告.md
├── 03-通用安装交付文档.md
└── urgent-execution/
    └── SKILL.md
```

> 两份文档保留在根目录，是为了让 `SKILL.md` 中的路径引用保持有效，也不影响已经安装到各宿主的核心文件哈希。

## 快速开始

| 宿主 | 技能文件 | 路由 / 适配 |
|---|---|---|
| Claude Code | `~/.claude/skills/urgent-execution/SKILL.md` | `~/.claude/CLAUDE.md` |
| DeepSeek Harness (DSH) | `.dsh/skills/urgent-execution/SKILL.md` | `.dsh/AGENTS.md` |
| OpenAI Codex | `~/.codex/skills/urgent-execution/SKILL.md` | `~/.codex/AGENTS.md` |
| DeepTutor | 账号级技能根 `<skills>/urgent-execution/SKILL.md` | 同根 `urgent-execution-router/SKILL.md`（`always: true`） |

> 各宿主版本的路径、配置文件和合并方式可能不同。安装前请先读 [03-通用安装交付文档.md](03-通用安装交付文档.md)，按实际版本确认根目录与入口，不要直接照抄路径。

## 使用方式

开启当前会话：

```text
【急急如律令】
请完成……
```

退出当前会话：

```text
【return 0】
继续……
```

口令必须**独占第一物理行**，前后不能有空格、引号、代码块标记或其他字符。第二行起才是任务正文。

## 激活协议

| 输入 | 结果 |
|---|---|
| 第一行精确为 `【急急如律令】` | 当前会话 ON；已经 ON 时保持 ON |
| 第一行精确为 `【return 0】` | 当前会话 OFF；已经 OFF 时保持 OFF |
| 其他消息 | 保持当前状态 |
| 第二行、引用、代码块中的口令 | 不切换 |
| 工具、后台任务、其他会话、子代理的消息 | 不切换（尽力判断） |

新会话和新分叉默认 OFF。全局安装不等于全局激活；其他会话需要各自输入口令。

## 安装等级与已知限制

这份仓库提供的是**共享核心 + 短路由**，属于文档定义的“尽力适配”：

- 没有宿主级来源钩子；消息是否来自本人，由模型结合可靠对话上下文判断；
- ON/OFF 状态由模型从可靠消息历史维持，不是宿主持久状态文件；
- 上下文压缩、恢复、重启后的状态保持是尽力而为，不保证；
- 引用、粘贴、工具输出里出现口令时，仍可能被误判。

要实现交付文档里的“可靠适配”，需要宿主级事件钩子、来源验证、会话状态存储和上下文注入；接口因宿主而异，详见 [03-通用安装交付文档.md](03-通用安装交付文档.md)。

## 验收

最小验收（详细 A01–A20 见 [02-编写迭代与验证报告.md](02-编写迭代与验证报告.md)）：

1. 新会话，不输入口令 → 默认 OFF；
2. 第一行 `【急急如律令】`，第二行一个小任务 → 进入 ON，任务立即开始；
3. 第一行 `【return 0】`，第二行继续任务 → 退出 ON，任务继续；
4. 把口令放在第二行、引用或代码块里 → 不切换；
5. 工具/后台消息里包含口令 → 应不切换（此条只能尽力，不是强制）。

## 兼容性

- 技能格式：Markdown + YAML frontmatter；
- 无运行时依赖，不绑定模型、API、工具名称或安装路径；
- 提供 Claude Code、DeepSeek Harness、OpenAI Codex、DeepTutor 的装载路径；行为验收项见 [02-编写迭代与验证报告.md](02-编写迭代与验证报告.md)；
- Windows / macOS / Linux 均可使用，路径按各自宿主规则解析。

## 版本与变更

当前版本：**1.0.0**。变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 贡献

欢迎 issue 和 PR。修改激活协议或执行策略时，请同步更新 `02` / `03` 文档与验收项；不要在多个宿主复制出互相漂移的执行规则。

## 许可证

本项目采用 [MIT License](LICENSE)。Copyright (c) 2026 Terry Yang.

## English summary

`urgent-execution` is a session-scoped Markdown skill for AI agents. A user message whose first physical line is exactly `【急急如律令】` turns the current session ON; `【return 0】` turns it OFF. New sessions start OFF, and other sessions are unaffected. The skill prioritizes time-to-verified-delivery without changing model endpoints, credentials, or permissions. It ships as a shared core plus thin per-host routes for Claude Code, DeepSeek Harness, OpenAI Codex, and DeepTutor; see the Chinese documents for host-specific installation paths and the distinction between strict and best-effort adaptation.
