#### `braintrust` — SaaS eval 平台

`braintrust` 是一个 SaaS 产品，提供 eval 即服务：托管的 golden set 存储、浏览 eval 结果的 UI、跨运行的回归比较、随时间的仪表盘、数据集版本管理，以及用于检测代码的 Python SDK。你针对 SDK 编写 eval 案例；结果流向托管平台；队友在 UI 中浏览、讨论和决定。


    from braintrust import Eval, init_dataset

    dataset = init_dataset(project="beacon-clinical", name="clinical_summary_v3")

    eval_result = Eval(
        "beacon-clinical-eval",
        data=lambda: dataset.iter(),
        task=lambda input: summarize_clinical_note(input["note"]),
        scores=[clinical_rubric_score, format_validity_score],
    )


相对 OSS 的增值是平台：托管存储、UI、PM 或临床医生（非工程师）浏览结果并在不设置本地基础设施的情况下提供反馈的能力。对于 eval 结果需要工程外利益相关者可见的团队，UI 是真实的生产力倍增器。

**适配**：超过约 5 名工程师的团队；eval 结果需要非工程师审查的团队；有 SaaS 预算且偏好不维护基础设施的团队。

**局限**：SaaS 成本（因团队规模和数据量而异；2026 年中等团队通常每月支付几百到几千美元）。数据驻留考虑（你的 eval 数据，包括任何生产样本，流向供应商服务器）。对于 HIPAA 敏感工作，需要 BAA 并增加供应商管理开销。

#### `langsmith` — LangChain 绑定的工作流

`langsmith` 是 LangChain 的第一方可观测性和评估平台。如果你的代码库构建在 LangChain 上，`langsmith` 以接近零摩擦集成：每次链调用产生跟踪；跟踪自动捕获；eval 对捕获的跟踪运行。


    from langsmith import Client
    from langsmith.evaluation import evaluate

    client = Client()
    results = evaluate(
        lambda inputs: summarize_clinical_note(inputs["note"]),
        data="clinical_summary_v3",
        evaluators=[clinical_rubric_evaluator],
    )


**适配**：技术栈是 LangChain 原生的团队；受益于统一可观测性加 eval 表面的团队；选择 LangChain 作为编排层的团队（带有第 25 章反模式节讨论的 trade-off）。

**局限**：在 LangChain 是你的编排层时最有用。对于选择更轻抽象（直接 provider SDK、Pydantic AI、自定义编排）的团队，`langsmith` 人体工程学较差。
