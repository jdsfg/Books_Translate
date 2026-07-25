> 本导读整理自 Socratopia 网站本书介绍页：https://www.socratopia.app/library/software-engineering-craft-en

软件工程匠艺（software engineering craft）的价值，过去常常被建立在“手写代码的成本”之上。到 2026 年，这个立足点崩塌了：一个 AI 助手能在十五分钟内产出一个 500 行的可用模块。于是有人说匠艺不再重要。他们错了，这本书就是对此的谨慎论证。瓶颈没有消失——它发生了转移。2016 年工程师的一天可能是 60% 写代码 / 20% 审阅 / 20% 维护；2026 年则是 20% / 40% / 40%。真正在新比例里“支付租金”的纪律——把测试当作规格（tests as spec）、在测试保护下重构（refactoring under test）、命名即设计（naming as design）、架构决策记录（ADRs）、代码审查（code review）、版本控制叙事（version-control narrative），以及把 AI 当作协作者（AI as collaborator）——才是本书真正要教的东西。

三位工作工程师贯穿各章。Asher Goldman 在 Trellis 是一名 Staff 工程师（Staff Engineer），面对八年历史的 CRM 代码库，他会在改动每一行令人意外的代码前先问“原作者在担心什么？”。Aki Tanaka 在 Helix 是一名高级工程师（Senior Engineer），她拒绝在测试还没变红时就打开 Claude Code——这个习惯源自某年秋天，一个智能体生成了六百行看起来合理的代码，却搞乱了 staging 环境的 webhook 状态，吃掉她两天加一个周日。Carmen Ortiz 在 Currents 是一名工程经理（Engineering Manager），她的每条审查评论都按标签优先（label-first）写法：Blocking:、Suggestion:、Decision needed:，让读者还没读正文就知道需要他做什么。他们反复出现，锚定在具体技术栈（TypeScript/Postgres、Rust/Cloudflare Workers、Python/FastAPI）和具体组织现实里，因此这些纪律落在真实代码上，而不是思想实验。

全书围绕“匠艺高于教条（discipline over dogma）”组织：每条规则都给出理由，以及何时可以打破它。TDD 那一章会诚实地承认先写后测（test-after）在什么时候是理性选择；模式那一章会点名哪些模式已经老去（Singleton、Visitor）以及为什么；大重写那一章既回顾 Joel Spolsky 的经典警告，也考察重写成功的案例。每个胜利旁边都坐着一个失败案例——Northwind 的账本迁移在 25% 流量处停滞并被放弃，与成功的并行路径重构（parallel-paths refactor）并列。线索 C（Thread C）贯穿第三到第八部分：LLM 在 2026 年最常撒的七种代码谎言——幸福路径偏见（happy-path bias）、过度抽象（over-abstraction）、风格不一致（inconsistent style）、缺失错误处理（missing error handling）、差一与边界错误（off-by-one boundary errors）、幻觉 API（hallucinated APIs）、看似可信的不安全代码（plausible-looking insecure code）——每一章都会指出本章的纪律能抓住哪一种，并在具体代码里演示；附录 D 把七种谎言汇总成一张可打印的 AI 代码审查清单。到最后一章，当 Asher、Aki 和 Carmen 汇聚到一个为期五个月的跨组织客户授权迁移项目时，这些纪律不再是抽象概念：你已经看着它们在三个真实工程语境里被实践了 23 章。

**目标读者（Target audience）**：有 2–10 年经验的工作软件工程师；想在代码审查中为直觉寻找词汇的工程经理；准备晋升的高级工程师；想跳过五年模式探索的初级工程师； onboarding 新团队的技术 lead；为代码健康提供咨询的顾问。

** prerequisites**：在任何语言里有一年的生产代码交付经验。习惯命令行、基本了解版本控制，并且愿意读代码而不是略读。