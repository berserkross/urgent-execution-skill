# Host installation sync · 2026-11-19

This report records the public-safe result of synchronizing `urgent-execution` 1.1.0 from the GitHub repository to the agent hosts installed on the target PC. It intentionally omits the Windows user name, absolute home paths, account workspace identifiers, credentials, endpoints, and chat contents.

## Source and artifact

| Item | Value |
|---|---|
| Repository | `berserkross/urgent-execution-skill` |
| Source commit | `574da6853213fd559d01450c6ec883da7bc218cd` |
| Skill version | `1.1.0` |
| Core file | `urgent-execution/SKILL.md` |
| SHA-256 | `3E2D8521FA249DA7C969D14811DA06B187D65BC1DBB3D86657409B051F000861` |
| Format | Markdown with YAML frontmatter |

The remote branch was fetched before installation. `HEAD` and `origin/main` both resolved to the commit above, so no local/remote merge was required.

## Hosts synchronized

| Host | Observed host version | Result | Skill registration | Global route |
|---|---:|---|---|---|
| OpenAI Codex | app-server 0.167.2 | Already on 1.1.0; confirmed current | `~/.codex/skills/urgent-execution/SKILL.md` | `~/.codex/AGENTS.md` |
| Claude Code | 2.1.316 in the test environment | Updated from 1.0.0 to 1.1.0 | `~/.claude/skills/urgent-execution/SKILL.md` | `~/.claude/CLAUDE.md` |
| DeepSeek Harness | 0.2.2-rc.5 | Updated from 1.0.0 to 1.1.0 | `$DSH_HOME/skills/urgent-execution/SKILL.md` | `$DSH_HOME/AGENTS.md` |
| DeepTutor | 1.7.2 | Updated from 1.0.0 to 1.1.0 | account-level skill root | `urgent-execution-router` with `always: true` |
| Shared agent mirror | host-independent | Updated from 1.0.0 to 1.1.0 | `~/.agents/skills/urgent-execution/SKILL.md` | Consumed by the host that owns this shared root |

All installed core files matched the repository artifact by SHA-256. The previous copy at each updated destination was retained as `SKILL.md.bak-20261119-before-v1.1.0`.

## Verification

| Check | Evidence | Status |
|---|---|---|
| Repository freshness | Local `HEAD` equal to fetched `origin/main` | Pass |
| Artifact integrity | Repository and five installed/shared core copies share the same SHA-256 | Pass |
| Route presence | DSH `AGENTS.md`, Claude Code `CLAUDE.md`, Codex `AGENTS.md`, and the DeepTutor router are present | Pass |
| Protocol behavior | Repository validator: 45 of 45 state-reducer checks | Pass |
| Fast parameter matrix | Repository validator: 40 of 40 combinations, manual choice precedence, documentation paths | Pass |
| DeepTutor discovery | DeepTutor's `SkillService` enumerated both `urgent-execution` and `urgent-execution-router` from the account skill root | Pass |
| Backups | Old 1.0.0 file retained before each update | Pass |
| Public-content scan | No matching API-key, GitHub-token, bearer-token assignment, or private-key patterns in the repository | Pass |

These checks prove file delivery, host registration where the host exposes a local catalog, route presence, and the protocol/speed logic. They do not prove source identity in a real prompt, recovery after host restart or context compaction, or a provider speed tier unless the host supplies those events and a serving-tier receipt.

## Compatibility boundary

The shared core remains provider-neutral. It contains no model ID, provider endpoint, account setting, or credential. This matters for DeepTutor in particular: the same installed skill should operate with DeepSeek, OpenAI-compatible models, a local Qwen model, Claude through a supported adapter, or another provider the host exposes. A provider-specific native Fast option is requested only when that host, model, and request path actually support it.

The skill and a native Fast mode are related but not equivalent:

- Native Fast changes the model-serving tier and normally costs more usage.
- `urgent-execution` changes workflow priorities: clarify sooner, parallelize useful work, avoid redundant approval loops, keep verification on the critical path, and deliver usable partial work while repairing defects.
- Markdown-only hosts receive the workflow policy. They do not gain a hidden provider speed tier merely by loading the skill.

## Output-token and latency risk

The skill does not make decoding faster by itself. Loading a longer skill body, resolving ambiguity, launching agents, or running extra verification can add prompt, tool, coordination, and final-response tokens. On short tasks this overhead can make total time longer. The existing measurements show that ON mode was slower than the standard workflow on three short Codex trials.

Use the mode when saved clarification, parallel work, avoidance of repeated approvals, or recovery from defects is likely to outweigh coordination overhead. Reassess per task type rather than assuming that a larger resource budget guarantees a shorter wall-clock time.

## Remaining validation

1. Open a fresh Claude Code session and confirm the skill appears after the host rescans its personal skill directory.
2. Open or refresh a DSH session and confirm the `skill` tool can load `urgent-execution`.
3. Start DeepTutor and confirm the Skills panel lists both the core and always-on router; the underlying service catalog has already enumerated both.
4. Run the A01–A20 matrix on each host when that host's trusted input and session APIs are available.
5. Run paired long, multi-step benchmarks before claiming a general wall-clock speedup. Keep short-task regressions in the report.

## Rollback

Restore each retained `SKILL.md.bak-20261119-before-v1.1.0` beside its updated core file. The routes did not change in this synchronization. Removing a route disables recognition; it does not turn an existing ON state into a global switch or cancel already authorized tasks.

