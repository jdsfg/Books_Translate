**答案：** 有用的 prompt：_我在为文档搜索助手评估 5 个模型：5K 输入 / 400 输出，每天 5K 次调用。给我成本比较和推荐。_ LLM 会产生一个表格和推荐。你验证 (a) 每 token 价格是否匹配 provider 的当前定价（LLM 会 hallucinate 价格），以及 (b) 算术——手动计算 25M × 3 美元/1M；如果 LLM 说 750 美元而非 75 美元，那恰好是 §2.8 的 _不能可靠做算术_ 故障。始终验证乘法。

**Q3.** _处理部分响应_。你的团队的结构化输出提取管道（第 7 章预览）用 `max_tokens=2000` 发起 API 调用。偶尔，响应以 `stop_reason="max_tokens"` 返回且部分 JSON 无法解析。设计一个恢复策略。指出两条不同的缓解路径。

提示

你可以提高上限并重试，或重构任务以适应。§3.4 有概念性答案。

**答案：** 两条不同的缓解路径：

**路径 1：提高上限并重试，有界升级。**


    def extract_with_escalation(prompt, schema, max_tokens_options=(2000, 4000, 8000)):
        for max_tokens in max_tokens_options:
            response = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                system=schema_system_prompt(schema),
            )
            if response.stop_reason == "max_tokens":
                continue
            return parse_and_validate(response.content[0].text, schema)
        raise RuntimeError("Extraction did not fit even at 8K tokens; task is too large.")


这可行但有两个缺点：(a) 成本随 `max_tokens` 线性增长，即使在不成功的尝试上（你每次都为截断的输出付费），以及 (b) 升级顶部的故障模式就是 _放弃_，没有优雅降级。

**路径 2：分解任务以适应。**


    def extract_in_chunks(prompt, schema):
        chunks = split_input_by_natural_boundaries(prompt)
        partial_results = []
        for chunk in chunks:
            response = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": chunk}],
                system=schema_system_prompt(schema),
            )
            partial_results.append(parse_and_validate(response.content[0].text, schema))
        return merge_extractions(partial_results, schema)


这更难工程化（你需要有意义的 chunking 策略和处理重叠和冲突的合并步骤），但它有正确的成本结构（每次调用小且有界）和正确的可扩展性故事（输入可以增长而不破坏调用形状）。

**推荐**：在生产中，优先选择路径 2。路径 1 的升级策略是掩盖架构问题（任务不适合一次调用）的创可贴；路径 2 的分解迫使你面对和解决问题。分解模式也是 map-reduce summarization（第 8 章）和 RAG 中的 chunked extraction（第 9 章）的基础。现在就锻炼这个肌肉。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？
