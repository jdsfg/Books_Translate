### 基础论文（5 篇）

1. **Attention Is All You Need** — _Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin；NeurIPS 2017。_ 这是将 Transformer 推上桌面的论文，你在 2026 年从 API 调用的每个工件都是它描述的架构的某种后代：多头自注意力、位置编码、此后坍缩为仅解码器堆栈的编码器-解码器框图。你不需要重新推导数学来发布产品，但应仔细读一遍使 _注意力头_、_KV 缓存_ 和 _上下文窗口_ 等词不再是魔法而开始成为数据结构。本书第 2 章直接在此论文之上构建工程师的心智模型；如第 2 章任何句子感觉动机不足，答案在此。慢慢读，带铅笔；论文短且图表值得凝视。

2. **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** — _Wei, Wang, Schuurmans, Bosma, Ichter, Xia, Chi, Le, Zhou；NeurIPS 2022。_ 命名现代最具影响力的 prompt 工程技术的论文。经验声明很窄——追加 _让我们一步步思考_（或更丰富的少样本推理链）提升算术和符号任务表现——但概念声明很大：模型中的潜在能力可通过你如何提问解锁，而非仅通过它如何训练。第 6 章回到此论文解释为何显式推理脚手架有效、为何花费 token、以及为何 2026 年推理模型（o1 风格和 Claude 扩展思考家族）最好理解为烘焙到后训练中的思维链而非根本性的新能力。为框架而读；技巧此后已打包进你可调用的 API。

3. **ReAct: Synergizing Reasoning and Acting in Language Models** — _Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao；ICLR 2023。_ ReAct 是给我们 _思考/行动/观察_ 循环的论文，你会在市场上每个 agent 框架中认出它。其经验贡献按今天标准适度——HotpotQA 和 ALFWorld 分数略好——但其架构贡献定义了一代：agent 是循环，循环交错推理文本与工具调用，模型在下一轮看到自己之前的推理作为上下文。第 13 章直接在此脚手架上构建 agent 循环，第 14 章（多步规划）检视原始 ReAct 论文暗示但未完全表征的故障模式——上下文膨胀、推理漂移、工具调用循环。如你只读一篇 agent 论文，读这篇。
