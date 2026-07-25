### 第二部分 — Agent 框架目录（第 15 章四个之外）

第 15 章为正文选了四个：LangGraph（LangChain 生态默认）、AutoGen（微软研究院的多 agent 对话框架）、Pydantic AI（轻量、类型安全）和 Anthropic MCP（工具集成协议）。推荐是有观点的：小团队新 agent 用 Pydantic AI 或手写；LangChain 商店用 LangGraph；便携工具集成重要处用 MCP。

更广的 2026 年格局包括以下参与者。表格简短；下面段落承载实质。

框架 | 定位 | 考虑何时 | 跳过何时
---|---|---|---
CrewAI | 带角色抽象的多 agent 团队 | "角色扮演 agent"的心智模型匹配你的设计直觉且你在快速原型 | 你需要生产级可观测性、自定义路由或对 agent 循环的精细控制
OpenAI Swarm（实验性） | 轻量多 agent 参考实现 | 你在 OpenAI 生态内且想在 Responses API 之上做多 agent 最小演示 | 你需要维护、支持的框架——Swarm 是明确的研究工件
Haystack 2 | RAG 优先编排带 agent 扩展 | RAG 是主导工作负载且你想要管道框架而非 agent 框架 | 重心是 agent 循环工作；Haystack 的管道更适合 RAG 而非开放式 agent
LlamaIndex | RAG 框架带轻量 agent 循环 | 你已用 LlamaIndex 做检索且想扩展而非替换 | 你尚未承诺 LlamaIndex——2026 年无强 agent 侧理由从这里开始
DSPy | Prompt 和程序优化（非严格 agent 框架） | 你需要原则性方式针对客观指标优化 prompt 和少样本示例 | 你想要运行时 agent 框架——DSPy 是编译器式工具，非运行时
Smolagents | Hugging Face 的最小基于代码的 agent 框架 | 你想要代码即行动空间（agent 写 Python 而非调用结构化工具）且你信任沙箱故事 | 你需要结构化工具调用、广泛提供商支持或打磨的生产故事

**CrewAI。** 中心抽象是"团队"——角色定义的 agent（"研究员"、"作者"、"编辑"）协同工作。优势是概念性的：角色模型干净地映射到产品团队描述他们想要什么的方式，使原型快速且对编写团队的 PM 和设计师可访问。弱点是与生产的差距：可观测性、自定义路由钩子和每轮循环的精细控制在 2026 年比 LangGraph 或 Pydantic AI 更薄。为 POC 采用 CrewAI 然后发布的团队常在更可配置的框架上重新实现。考虑用于早期探索；如你扩展预期迁移。
