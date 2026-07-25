### 书籍（5 本）

11. **Designing Machine Learning Systems** — _Chip Huyen；O'Reilly，2022。_ 在 LLM 改变一切之前写的，但关于 ML 系统设计的基础问题——数据管道、训练-服务偏差、监控、MLOps 生命周期——仍然完全适用。本书第 16-21 章在生产架构和运维上隐式建立在 Huyen 的框架上。读它用于 LLM 时代之前的 ML 系统工程基础。

12. **Building Effective Agents** — _Anthropic；作为长篇工程指南发表于 anthropic.com，2024 年 12 月。_ Anthropic 自己的 agent 工程田野指南，从前沿实验室观察客户用其 API 构建的视角写成。指南异常清晰地说明什么有效（小型、可组合、可审查的工作流；工具使用；_增强 LLM_ 基线）和什么无效（过度工程的多 agent 系统而简单模式即可；因无人设预算而循环的 agent）。本书第 13、14 和 15 章反复依赖此指南——它是截至 2024 年底领域最接近 agent 设计共识的东西——你应为模式和姿态都读它。Anthropic 发布少量此类长篇工程指南；关注公司工程博客获取更新。

13. **AI Engineering: Building Applications with Foundation Models** — _Chip Huyen；O'Reilly，2025。_ Huyen 的第二本书，明确为 LLM 时代而写。它在范围和某些模式上与本书重叠——RAG、eval、agent、prompt 工程、推理经济——且值得作为相邻的、有时互补的论述阅读。本书倾向于实例叙事和少量反复案例研究（Beacon Health AI、Strata Research、Helios），Huyen 倾向于更广的调查覆盖和参考文献。两本书在某些地方不同——最明显在 agent 成熟度和教多少微调——且分歧是有益的；两本都读并形成自己的观点。如你读完本书想以不同声音再过一遍同样材料，这是接下来该拿起的书。

14. **Eugene Yan 的文章合集** — _Eugene Yan；eugeneyan.com，2019 至今。_ Eugene Yan 是当一个在 Amazon 工作的 ML 工程师决定深入写他发布的一切时会发生的事。他关于 LLM 评估、RAG 模式、推荐系统和应用 ML 系统设计的文章已成为许多 AI 团队的必读；仅 _构建基于 LLM 的系统和产品的模式_ 一文就比大多数已出版书籍更实用。本书第 7 章（嵌入和向量搜索）引用 Yan 的写作作为经典 IR 胜过向量的例子，第 24 章（知道何时不使用 AI）吸收他反复坚持的好 ML 工程始于清晰问题陈述和可能工作的最便宜基线。整个网站是免费工程图书馆；浏览目录，然后读所有看起来与你本季度发布相关的。
