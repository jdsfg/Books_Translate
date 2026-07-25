#### 模式 1：查询扩展

在检索前向查询添加同义词、相关术语或改述。做好时，扩展捕获字面查询会遗漏的相关块。

    def expand_query(query: str) -> str:
        expansion_prompt = f"""用同义词和相关术语扩展以下查询。
    只输出扩展后的查询。

    Query: {query}
    Expanded query:"""
        expansion = small_llm.complete(expansion_prompt, max_tokens=100, temperature=0)
        return f"{query} {expansion}"


成本：每查询一次小 LLM 调用（工作马层级模型亚美分）。延迟：约 200ms（相对于总检索管道可忽略）。

#### 模式 2：HyDE（假设文档嵌入）

Gao 等 2022。不嵌入查询，而是请 LLM 生成查询的 _假设答案_，然后嵌入假设答案。假设答案比查询更类似于检索目标（它们也是答案/段落）。

    def hyde_retrieve(query: str) -> list[Chunk]:
        hypothetical_prompt = f"""写一个对这个问题的简短假设答案。
    Question: {query}
    Answer:"""
        hypothetical = small_llm.complete(hypothetical_prompt, max_tokens=200, temperature=
0)                                                                                                 hypothetical_vec = embed(hypothetical)
        return vector_db.search(hypothetical_vec, top_k=20)


HyDE 通常在基准任务上提升检索 recall 3–7 分；成本是一次额外 LLM 调用。对于高质量生产 RAG，通常值得。

#### 模式 3：查询分解

一次问多件事的复杂查询（_"育儿假策略是什么以及它如何与丧假策略交互？"_）被分解为子查询；每个子查询有自己的检索；LLM 从并集合成。

    def decompose_and_retrieve(query: str) -> list[Chunk]:
        decomp_prompt = f"""将这个问题分解为 1-3 个更简单的子问题，每行一个。

    Question: {query}"""
        sub_questions = small_llm.complete(decomp_prompt).split("\n")
        all_chunks = []
        for sq in sub_questions:
            all_chunks.extend(hybrid_search(sq, top_k=5))
        return deduplicate(all_chunks)


分解在单查询检索遗漏用户问题一个方面时帮助。成本：一次分解调用加多次检索。对于复杂查询，成本合理；对于简单查询，开销浪费。
