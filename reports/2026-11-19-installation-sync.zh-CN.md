# 四宿主部署同步 · 2026-11-19

本报告公开记录 `urgent-execution` 1.1.0 从 GitHub 同步到目标 PC 上各 Agent 宿主的结果。内容已去除 Windows 用户名、绝对主目录、账号工作区标识、凭据、接口地址和聊天内容。

## 来源与产物

| 项目 | 值 |
|---|---|
| 仓库 | `berserkross/urgent-execution-skill` |
| 来源提交 | `574da6853213fd559d01450c6ec883da7bc218cd` |
| 技能版本 | `1.1.0` |
| 核心文件 | `urgent-execution/SKILL.md` |
| SHA-256 | `3E2D8521FA249DA7C969D14811DA06B187D65BC1DBB3D86657409B051F000861` |
| 格式 | Markdown + YAML frontmatter |

安装前先拉取了远端分支。本地 `HEAD` 与 `origin/main` 均为上述提交，因此没有额外的合并动作。

## 已同步宿主

| 宿主 | 观察到的版本 | 结果 | 技能位置 | 全局路由 |
|---|---:|---|---|---|
| OpenAI Codex | app-server 0.167.2 | 原本已是 1.1.0，已确认一致 | `~/.codex/skills/urgent-execution/SKILL.md` | `~/.codex/AGENTS.md` |
| Claude Code | 测试环境为 2.1.316 | 从 1.0.0 更新到 1.1.0 | `~/.claude/skills/urgent-execution/SKILL.md` | `~/.claude/CLAUDE.md` |
| DeepSeek Harness | 0.2.2-rc.5 | 从 1.0.0 更新到 1.1.0 | `$DSH_HOME/skills/urgent-execution/SKILL.md` | `$DSH_HOME/AGENTS.md` |
| DeepTutor | 1.7.2 | 从 1.0.0 更新到 1.1.0 | 账号级技能根 | `urgent-execution-router`，`always: true` |
| 共享 Agent 镜像 | 与宿主无关 | 从 1.0.0 更新到 1.1.0 | `~/.agents/skills/urgent-execution/SKILL.md` | 由使用该共享根的宿主读取 |

所有已安装核心文件都与仓库产物的 SHA-256 完全一致。每个被更新的位置都保留了旧文件：`SKILL.md.bak-20261119-before-v1.1.0`。

## 验证结果

| 检查 | 证据 | 结果 |
|---|---|---|
| 仓库是否最新 | 拉取后本地 `HEAD` 等于 `origin/main` | 通过 |
| 文件完整性 | 仓库文件与五个已安装/共享副本 SHA-256 一致 | 通过 |
| 路由是否保留 | DSH `AGENTS.md`、Claude Code `CLAUDE.md`、Codex `AGENTS.md` 和 DeepTutor router 均存在 | 通过 |
| 协议逻辑 | 仓库校验器 45/45 状态函数检查 | 通过 |
| 速度参数矩阵 | 仓库校验器 40/40 组合、手动优先及文档路径检查 | 通过 |
| DeepTutor 发现 | DeepTutor `SkillService` 从账号技能根枚举出 `urgent-execution` 与 `urgent-execution-router` | 通过 |
| 回滚材料 | 每个更新点均保留旧 1.0.0 文件 | 通过 |
| 公开内容扫描 | 仓库内未命中 API key、GitHub token、Bearer token 赋值或私钥特征 | 通过 |

上述检查证明文件交付、可观察的宿主注册、路由存在以及协议/速度逻辑。它们不证明真实消息来源鉴别、宿主重启或上下文压缩后的恢复，也不证明服务商实际使用了某个速度档位；这些必须有宿主事件和服务端档位回执。

## 适配边界

共享核心继续保持供应商中立，不包含模型 ID、服务商 endpoint、账号设置或凭据。对 DeepTutor 尤其如此：同一份技能应可在 DeepSeek、OpenAI 兼容模型、本地 Qwen、经支持的 Claude 适配层，或宿主实际暴露的其他供应商上工作。只有宿主、模型和请求入口真正支持原生 Fast 时，才请求供应商专属速度档位。

本技能与原生 Fast 有联系，但不等价：

- 原生 Fast 改变模型服务档位，通常消耗更多额度。
- `urgent-execution` 改变工作流优先级：更早澄清、按收益并行、减少重复请示、把验证放进关键路径，并在修复时交付可用部分。
- 只能加载 Markdown 的宿主获得工作流策略，不会因加载技能而自动得到隐藏的供应商加速档。

## 输出 token 与延迟风险

技能本身不会提高模型解码速度。加载较长的技能正文、澄清问题、启动代理、运行额外验证或输出更多状态说明，都会增加提示词、工具、协调和最终答复 token；短任务因此可能变慢。现有 Codex 短任务实测中，ON 组反而比普通工作流更慢。

只有在节省关键澄清、并行工作、避免重复审批或减少返工预计能抵消协调开销时才应开启。应按任务类型复测，不能把“额度更多”当作“墙钟时间必然更短”的保证。

## 尚待现场确认

1. 新开 Claude Code 会话，确认宿主重新扫描个人技能目录后能看到该技能。
2. 打开或刷新 DSH 会话，确认 `skill` 工具可读取 `urgent-execution`。
3. 启动 DeepTutor，在 Skills 面板确认核心与 always router 均出现；其底层服务目录已成功枚举两者。
4. 在宿主可信输入和会话 API 可用时，执行 A01–A20 行为矩阵。
5. 在宣称普遍提速前，运行长耗时、多步骤的成对基准，并保留短任务退化数据。

## 回滚

把每个更新点旁的 `SKILL.md.bak-20261119-before-v1.1.0` 恢复为该目录的 `SKILL.md`。本次没有修改路由。删除路由只会关闭口令识别，不会把已有 ON 变成全局开关，也不会取消已授权的任务。

