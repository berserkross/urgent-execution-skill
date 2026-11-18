# 跨宿主测速 · 2026-11-19

本次检查使用通用技能 v1.1.0。所有计时以秒计。每组的验收通过数包含格式检查，样本量较小。表中耗时为所有获得完成时间的样本中位数；没有成功启动的作业列在逐次记录中。

| 宿主 | 任务 | 状态 | 完成计时数 | 验收通过 | 整轮中位数（范围） | 最终答复首段出现 | 可见输出跨度 | 估算 token/s |
|---|---|---|---:|---:|---|---:|---:|---:|
| cc | sequence | bare | 5 | 5 | 4.30（3.49–4.70） | 2.41 | 1.30 | 245.20 |
| cc | sequence | off | 5 | 5 | 3.98（3.86–4.87） | 2.09 | 1.32 | 243.20 |
| cc | sequence | first | 5 | 5 | 6.26（5.32–6.68） | 4.24 | 1.31 | 245.00 |
| cc | sequence | continued | 5 | 5 | 4.08（3.89–4.62） | 2.17 | 1.31 | 244.10 |
| cc | review | bare | 5 | 5 | 4.58（4.15–5.47） | 3.97 | 0.04 | — |
| cc | review | off | 5 | 5 | 4.57（4.08–6.52） | 3.97 | 0.04 | — |
| cc | review | first | 5 | 5 | 6.30（5.73–6.67） | 5.71 | 0.03 | — |
| cc | review | continued | 5 | 3 | 4.98（3.91–5.79） | 4.36 | 0.05 | — |
| cc | repair | bare | 5 | 5 | 3.41（2.83–3.80） | 2.48 | 0.04 | — |
| cc | repair | off | 5 | 5 | 2.80（2.71–4.32） | 2.17 | 0.02 | — |
| cc | repair | first | 5 | 5 | 5.30（4.92–6.34） | 4.41 | 0.02 | — |
| cc | repair | continued | 5 | 5 | 2.93（1.92–3.35） | 2.33 | 0.04 | — |
| dsh | sequence | bare | 1 | 1 | 4.33（4.33–4.33） | — | — | — |
| dsh | sequence | off | 1 | 1 | 3.49（3.49–3.49） | — | — | — |
| dsh | sequence | first | 1 | 1 | 6.72（6.72–6.72） | — | — | — |
| dt | sequence | off | 1 | 1 | 20.87（20.87–20.87） | — | 0.75 | 425.00 |
| dt | sequence | first | 1 | 1 | 19.32（19.32–19.32） | — | 0.72 | 442.60 |

bare 为临时配置无技能，off 为加入核心和路由但未提交口令，first 为新会话首行提交 ON，continued 为恢复前一会话的下一轮。实验使用脚本提交测试夹具，只验证宿主在该入口表现出的行为，不证明本人消息来源鉴别。

Claude Code 使用本机 SDK 自带 CLI 和现有网关配置。每次在临时目录启动 CLI，四组按轮交错。sequence 输出固定 1–160 数列；review 用 Read 读取两个独立文件后计算净额；repair 要求给出通过约定的修复表达式。continued 会在同一会话重复同题，可能受上下文复用和答案复用影响。

Claude Code 的首段时间从启动客户端计至最终回答的首个文本增量，包含启动、技能、工具和推理等待。估算 token/s 使用最后一条模型消息的输出 token 减去 thinking token，再除以首末文本增量间隔；首个增量本身已有文本，客户端可能缓冲，故不能当作 GPU 解码吞吐。只对精确通过数列验收的样本计算该值。

DSH 和 DT 的耗时来自统一委派入口的子进程计时，与 CC 启动计时不能直接横比。DSH/DT 的资料验收夹具使用内联记录，修复夹具使用 Python 表达式和数值测试。工具集、模型以及计时原点不同，比较均以同宿主为限。

## 实测配置、能力与未完成项

Claude Code 2.1.316 使用现有网关模型 DeepSeek V4 Pro（通过网关）。显式以 fastMode=true 请求同一模型，任务成功，usage.service_tier 返回 standard。60 次任务中 15 次首次开启均调用 Skill，普通与关闭组没有调用 Skill。持续组有两次复用历史答案而未按要求重读两个文件，故计为指令执行失败。Anthropic 官方 /fast 的入口、适用模型、账号和网关条件见 [Claude Code Fast](https://code.claude.com/docs/en/fast-mode)。本测试没有验证 Anthropic 原生模型账号。

DSH 0.2.2-rc.5 的 headless 使用 deepseek-flash。三种新会话条件各有一条通过的长输出样本，缺少服务档回执和对应的分段计数，不能据此判断解码性能或确认首次组加载了核心。

DeepTutor 1.7.2 隔离 chat 产生了两个各含 320 个可见 token 的单次样本。两次均为一次模型调用、零工具步骤，未取得可靠证据证实核心已被加载。CSV 保留了 DT 自报的首 token 延迟及含推理 token 的 completion 吞吐，并区分了按可见内容事件时间估算的速度。先前 deep_research 探针缺少 mode、depth；常规 chat 另有一次事件序号冲突，即使外层退出成功也已排除。

现有 DT 目录包含 DeepSeek、OpenAI 兼容网关和本地 Qwen 配置，本轮实际运行的是 DeepSeek。未验证其他账户或提供商。OpenAI 原生 Fast 需要请求入口支持并以服务端实际档位核对；兼容网关需逐个验证。DeepSeek 的 thinking/推理强度与切换模型会改变比较条件。Ollama 可按模型、自身推理设置与运行硬件分别测量。未来 Claude 接入应看中间层是否传递服务商的速度选项。[OpenAI Fast](https://developers.openai.com/api/docs/guides/fast-mode) · [DeepSeek 接口](https://api-docs.deepseek.com/api/create-chat-completion/)

本机同时出现持续的低空闲内存。统一入口要求 DSH 至少 1024 MB、DT 至少 1536 MB。多次复查、串行重试仍被拒绝，最近一轮 DSH 拒绝时仅余 425–507 MB。因此 DSH/DT 尚无完整每组五次、持续 ON、文件检索与修复任务的可比较结果。DT 的统一入口还没有把恢复会话参数传给子程序。报告中的 first 只表示测试端提交口令，表中没有词元级证据的栏位保持空白。

[逐次测量 CSV](trials.csv)。rep 从 0 起计。ms、first_ms 和 span_ms 以毫秒计，provider_ttft_s 以秒计。空白表示没有测量值。内存不足而未启动的记录保留在 CSV，未纳入耗时中位数。
