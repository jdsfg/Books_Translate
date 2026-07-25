**OpenAI Swarm（实验性）。** OpenAI 发布的极简多 agent 参考实现，展示 agent 间交接和轻量编排。它有意为研究工件而非生产框架——无支持 SLA，无稳定 API 保证，文档明确声明实验状态。价值在于教学：阅读源码（很短）以理解多 agent 交接的最小机制。如你在 OpenAI 生态内且想在 Responses API 之上快速演示多 agent，Swarm 是最低摩擦起点。不要在此基础上构建生产系统；它不会获得 LangGraph 或 Pydantic AI 那样的维护投入。

**Haystack 2。** deepset 的框架，重心在检索和文档处理；管道组合检索器、排序器、prompt 构建器和生成器为有向图，类似上面模式 3。Agent 扩展将管道包装为 LLM 可调用的工具。成熟、文档良好、有清晰部署故事（Haystack-as-a-Service，或 FastAPI 下自托管）。当 RAG 是主导工作负载且团队偏好管道心智模型而非图或类型函数心智模型时考虑。当 agent 工作是主要事情且 RAG 是子组件时跳过；LangGraph 或 Pydantic AI 在那里更合适且你自己组合检索。

**LlamaIndex。** 最初为 2022 年的 GPT Index，LlamaIndex 是长期存在的 RAG 框架，逐渐生长了 agent 层（最初 ReAct 风格，然后更通用运行时，然后 2024-25 年类似 LangGraph 图的"工作流"）。检索侧优秀——广泛连接器、成熟查询引擎、强开箱即用性能。Agent 侧称职但在 2026 年缺乏相对 LangGraph 或 Pydantic AI 的清晰差异化。如你已在 LlamaIndex 做检索，用其 agent 层扩展而非添加第二个框架。全新项目，仅 agent 侧不是从这里开始的理由；先选 agent 框架再分别选检索栈。

**DSPy。** 非严格 agent 框架——一种编程模型，开发者写带声明输入/输出签名的"模块"，DSPy 通过针对开发者提供的指标优化 prompt 和少样本示例来编译它们。与四个正文框架的关系是正交的：DSPy 可产生 LangGraph 节点或 Pydantic AI agent 使用的 prompt。优势是原则性优化——给定清晰指标和有意义的训练示例，DSPy 找到手写难以匹配的 prompt 配置。弱点是编译是单独阶段；你编译、发布工件、在不同框架上运行。当你有可测量目标、你信任的 eval 集和额外构建阶段的带宽时考虑。当你需要运行时框架时跳过——DSPy 是错误层。
