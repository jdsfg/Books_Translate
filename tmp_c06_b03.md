#### `inspect-ai` — 安全 eval 专家

`inspect-ai` 是由英国 AI 安全研究所发布的开源 eval 框架。它为安全评估而构建：能力评估、危险能力探测、prompt 注入稳健性、拒绝模式合规。设计强调可复现性（完整转录保存；确定性重放）、来源（每个分数可追溯到产生它的输入）和可组合性（eval 定义是组合成更大套件的 Python 对象）。


    from inspect_ai import Task, eval, task
    from inspect_ai.dataset import Sample
    from inspect_ai.solver import generate
    from inspect_ai.scorer import answer

    @task
    def clinical_summary_safety():
        return Task(
            dataset=load_clinical_dataset("goldens/clinical_summary/"),
            plan=[generate(model="claude-sonnet-4-20260315")],
            scorer=answer(grader="exact"),
        )

    eval(clinical_summary_safety, model="claude-sonnet-4-20260315")


输出是每个输入、每次模型调用、每个分数的结构化日志。日志是你保存、审计和重放的制品。对于受监管的工作（Beacon Health AI 的 HIPAA 约束临床管道；国防和政府工作），审计跟踪是真实功能。

**适配**：做安全相关评估的团队；需要完整审计跟踪以符合监管合规的团队；想要显式为对抗和能力评估设计的框架的团队。

**局限**：比 `pytest-evals` 更重。框架有主张；你在框架的惯语中写 eval，而非你的 pytest 惯语。学习曲线更陡。

#### `ragas` — RAG 专家

`ragas` 专为 RAG 评估构建。该库实现了标准 RAG eval 指标：_忠实度_（答案是否从检索上下文得出？）、_答案相关性_（答案是否针对问题？）、_上下文精确率_（检索块是否包含相关信息？）、_上下文召回率_（检索是否找到了相关信息？）。所有四个都由底层 LLM 作为评判者调用评分，带合理默认值。


    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_re
call                                                                                       
    dataset = load_rag_dataset("goldens/strata_legal/")
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatAnthropic(model="claude-sonnet-4-20260315"),
    )


指标在 RAG eval 意义上是 _有主张的_：它们捕获了自 2023–2024 年 RAG eval 文献以来成为标准的四轴分解。如果你的评估是 RAG 形态的，`ragas` 节省数周的指标设计工作。

**适配**：任何做认真 RAG 评估的团队；Strata Research 是范式案例。该库的指标是正确的起点且通常是正确的终点。

**局限**：在 RAG 之外，该库不适用。对于 agent 评估、结构化输出评估、语音助手评估等，`ragas` 不是你的工具。
