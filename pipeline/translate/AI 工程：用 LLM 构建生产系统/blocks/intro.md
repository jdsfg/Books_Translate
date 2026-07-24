> 本导读整理自 Socratopia 网站本书介绍页：https://www.socratopia.app/library/ai-engineering-en

那个事件——锚定在第 14 章——是本书用作警示固定点的六起真实或复合失败案例之一。围绕这些案例，本书构建了一套纪律。2026 年的 AI 工程不是 prompt 调试，不是 LangChain 管道拼接，也不是等待下一个模型发布来修复已有的问题。它是一种针对你不拥有的随机性组件的工程实践——eval 驱动、成本感知、observability 优先、设计上有界。

本书最想植入的一个习惯是：对于你做出的每一个架构选择，你都应该能回答四个正交问题——模式是什么？eval 是什么样的？它在生产环境中如何失败？成本是多少？这四个问题成为每一章的主线。它们是 AI 工程师与只交付过一个 demo 的人之间的区别。

三个生产案例贯穿 25 章。Beacon Health AI 构建了一个受 HIPAA 约束的临床笔记摘要系统，其中 eval 集本身就是 PHI，而 observability 带来了 BAA 合规张力。Strata Research 走过了一段法律科技 RAG 之旅，pass rate 在十二个月内从 43% 提升到 81%——没有突破性进展，没有单一技巧，只是持续应用四个杠杆（chunking、embedding、retrieval、ranking）加上一个能捕获每次回归的 eval。Helios Customer AI 运营着一个企业级 agent 平台，月处理 1000 万工单，月推理成本超过 100 万美元，deflection rate 达到 63%，并具备按租户的预算治理。读到最后，你会认出他们的决策就是你自己的决策。

你带走的不只是一份综述。而是十五个可落地的工作流（GitHub Actions 中的 eval-as-CI；带 A/B/C 结果的版本化 prompt 注册表；bounded-agent 设计文档；带按租户配额的 LiteLLM router 配置；带盈亏平衡计算的 Anthropic prompt caching；四层 prompt 注入防御；以及另外十个）——每一个都是你周一早上就能交付的生产级工件。四个附录收束全书线索：一份 15 篇论文的阅读清单、一个包含十种参考架构及 agent 框架的目录、一份 280 条术语的 glossary，以及一份为团队自审校准的七项 anti-pattern 速查表。如果你读完本书后，那四个问题已经成为本能反应，这本书就成功了。

**目标读者**：正在转向 AI 产品工作的软件工程师和 ML 工程师；正在设计 AI 功能的技术负责人和工程经理；构建 LLM 驱动创业公司的创始人；在成熟公司中增加 AI 功能的资深工程师；2026 年寻求 AI 工程职位的初级工程师

**前置要求**：Python 熟练（B142《AI 时代的 Python 编程》或同等水平）；对 LLM 有概念性了解（B058《AI 科学 I》或同等水平）；API 思维 + JSON + 基础后端工程。不需要 ML 博士学位。

**学习时长**：约 90–110 小时（25 章，每章约 3.5–4.5 小时，含练习及完整解答）