> **截至 2026 年。** 以下美元数字的快照日期：2026 年中。Anthropic Claude Sonnet 4 为 3.00 美元/百万新输入 + 0.30 美元/百万缓存读取 + 15.00 美元/百万输出；OpenAI GPT-4o 为 2.50 美元/10.00 美元；Gemini 2.5 Flash 为 0.10 美元/0.40 美元；DeepSeek V3 为 0.27 美元/1.10 美元。在你将这些复制到预算电子表格之前，检查 provider 的当前定价页面；这些数字每季度漂移。API 调用实际做什么的心智模型是值得牢记的部分。

Aiyana 在 Beacon Health AI 新角色中的第一次提交是四十三行 Python。关键的六行是这些：

    from anthropic import Anthropic

    client = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20260315",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    print(response.content[0].text)


这就是整个 API。你在本书中看到的一切都围绕那个调用封装。Streaming 封装它。工具调用封装它。RAG 封装它。Agent 封装它。生产 observability 封装它。但调用本身是六行，你应该能在睡梦中写出来。

本章拆解那六行，然后用你在生产中实际会转的完整旋钮集将它们重新组装。到最后你将知道 chat-completions 调用上每个参数做什么、何时设置它何时保留默认值、如何读取速率限制头、如何处理故障模式，以及你刚做的调用的账单是什么样的。

这是工程师的第一个工具。拿起来。

---
