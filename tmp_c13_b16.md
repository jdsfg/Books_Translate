当检索从文档返回块时，系统检查文档的整体处理完整性：

    def query_with_completeness_flag(query: str) -> QueryResult:
        retrieved = retrieve(query)
        docs_involved = {chunk.document_id for chunk in retrieved}
        incomplete_docs = [
            doc for doc in docs_involved
            if get_page_processing_status(doc) < COMPLETENESS_THRESHOLD
        ]
        answer = generate(query, retrieved)
        flags = []
        if incomplete_docs:
            flags.append(f"文档 {incomplete_docs} 有未处理页面；答案可能不完整。")
        return QueryResult(answer=answer, flags=flags)


用户在 UI 中看到标记；可选择验证或忽略。

(d) **文档隔离策略**：

当文档首次被摄取时，管道计算其完整性比率。完整性 < 95% 的文档不加入生产索引。它们留在隔离队列中。操作员（或用更强模型的自动化流程）尝试恢复；一旦完整性 >= 95%，文档移入生产。

这防止低质量文档污染生产索引，同时允许它们被修复。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_为视觉优先摄取管道工程化失败页面处理：跟踪、恢复、查询时暴露、隔离策略。_ 你验证 (a) SQL schema 捕获你的管道产生的实际运营数据（LLM 可能发明字段；对照你的管道能填充的检查），以及 (b) 用户面向标记措辞在失败页面无关紧要的文档上不会不必要地惊吓用户。

**Q4.** _成本优化多模态摄取_。你的初始视觉优先摄取估算 5 万美元。找到三个具体优化以减少 50% 而 eval 上质量损失不超过 2 分。

**答案：** 三个优化：

1. **批处理**：通过批端点路由摄取（Anthropic、OpenAI 都提供约 50% 折扣）。文档摄取是异步且可隔夜接受的；批处理是自然适配。**节省**：约 25K 美元（总额 50%）。质量影响：零（同模型、同 prompt）。
2. **分辨率控制**：从 600 DPI 降到 250 DPI（对大多数打字文本文档足够）。**节省**：约 5K 美元（视觉 token 大致随图像面积缩放；更低分辨率削减视觉 token 使用约 40%）。质量影响：涉及小文本的任务 0–1 分；标准任务 0 分。值得在 1K 页样本上试点验证。
3. **语料库分层**：80% 文档是典型打字内容（用更便宜的 Haiku Vision）；20% 是视觉复杂（多语言、手写、布局密集；用 Sonnet 4 Vision）。**节省**：约 10K 美元。质量影响：80% 层 1–2 分（Haiku Vision 在文本提取上稍不可靠）；20% 层约零。净质量影响约 1 分。

合计：25K 美元 + 5K 美元 + 10K 美元 = 节省 40K 美元；总额约 10K 美元而非 50K 美元。质量影响约 1–2 分，远在 2 分预算内。
