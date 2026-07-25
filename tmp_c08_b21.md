**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_我在将遗留散文 + 正则解析管道迁移到 `instructor` + JSON schema。概述迁移步骤、并行运行纪律和两个特定风险。_ 你验证 (a) 提议的并行运行逻辑实际保持下游契约（写一个契约测试确认两个管道在代表性输入上产生相同字典形态），以及 (b) 风险列表特定于你的管道（LLM 给通用列表；你定制）。

**Q5.** _决策：`instructor` + 原生 JSON schema vs. `outlines`_。对每个场景，推荐一个并用三点论证。

(a) 开源模型（Llama 3.3 70B）在 vLLM 上自托管，从笔记中提取临床实体。Pydantic 优先代码库。(b) Anthropic Sonnet 通过 API，从发票中提取结构化条目。Pydantic 优先代码库。(c) 一个研究项目，输出必须符合上下文无关文法（带特定方言子集的有效 SQL 查询）。(d) 一个小团队（4 名工程师）大规模运行 OpenAI gpt-4o-mini；输出是带三个变体的 Pydantic 判别联合。

提示

§7.3 和 §7.5 是选择面。推荐取决于（provider 原生 vs. 自托管）和（JSON schema vs. 更丰富约束）。

**答案：**

(a) **`outlines`。** (1) 自托管 vLLM 没有原生 provider 侧 JSON schema 模式；你需要一个包装 logit 级约束的库。(2) `outlines` 与 vLLM（及其他开源模型运行时）干净集成；这是其最强用例。(3) Pydantic 优先没问题：`outlines` 接受 Pydantic schema 并产生 Pydantic 验证输出，团队现有的类型卫生延续。

(b) **`instructor` + 原生 JSON schema。** (1) Anthropic 的原生工具使用结构化输出（§7.2）在 provider 侧经过良好优化；使用 `instructor.from_anthropic` 启用该路径而无需你实现约束层。(2) Pydantic 优先：`instructor` 直接返回 Pydantic 对象；零包装代码。(3) 约束在 provider 侧比客户端侧成本和可靠性更好；重试无 token 往返因为约束在发出前强制。

(c) **`outlines`。** (1) 原生 JSON schema 模式仅限 JSON；SQL 文法约束不可表达。(2) `outlines` 支持上下文无关文法约束（其 `outlines.grammar` 模块），这是精确工具。(3) 研究上下文开销可接受；文法级约束的精度超过客户端运行约束的运营复杂性。

(d) **`instructor` + 原生 JSON schema。** (1) OpenAI 的原生结构化输出模式（`response_format`）干净处理判别联合；schema 由 provider 强制。(2) 小团队加规模化等于优化运营简单性；`instructor` 是最轻触库。(3) 三变体判别联合是 `instructor` 的 `response_model` 参数的教科书适配；你获得验证、重试和类型化输出而无需写约束逻辑。
