# Changelog

本项目的重要变更记录在此文件中。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- README 增加“为什么用这个口令”一节，说明低频词、全角中括号与首行独占的误触发防护。
- README 补充安装验证措辞的澄清。
- `INSTALL.md` / `INSTALL.zh-CN.md`：四宿主手动安装步骤与 Agent 自安装 prompt。
- README（中英）增加“让 Agent 自己安装”小节，并链接 INSTALL 文档。

### Changed

- 默认 README 改为英文 `README.md`；原中文版移至 `README.zh-CN.md`，两版顶部增加语言切换。

## [1.0.0] - 2026-11-11

### Added

- `urgent-execution/SKILL.md`：共享核心，定义首行口令、会话状态与 ON 执行策略。
- `03-通用安装交付文档.md`：通用安装流程、Claude Code / DSH 适配路线与参考状态函数。
- `02-编写迭代与验证报告.md`：设计决策、45/45 状态函数检查、待验收项与性能比较方案。
- 首次公开发布。
