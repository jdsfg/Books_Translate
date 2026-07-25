#### 模式 4：自查询检索器

对于带结构化元数据约束（管辖权、日期、文档类型）的查询，使用 LLM 将自然语言查询解析为结构化搜索过滤：

    from datetime import date
    from pydantic import BaseModel

    class SearchFilters(BaseModel):
        semantic_query: str
        jurisdiction: list[str] = []
        effective_date_before: date | None = None
        effective_date_after: date | None = None
        document_types: list[str] = []


LLM（小模型即可）将 _"2023 年加州消费者保护法是什么？"_ 解析为：

    SearchFilters(
        semantic_query="consumer protection law",
        jurisdiction=["CA"],
        effective_date_before=date(2024, 1, 1),
        effective_date_after=date(2022, 12, 31),
    )


检索系统然后在向量搜索前应用元数据过滤（第 10 章 §10.5）。自查询检索器对任何在丰富元数据语料库上的 RAG 必不可少。

### 11.3 知识图谱 RAG：在素养深度

知识图谱 RAG（KG-RAG）用结构化知识图谱增强向量检索：实体、关系、属性。图谱编码扁平向量检索遗漏的领域特定结构。

模式：

1. **构建图谱**：从语料库提取实体和关系（NER + 关系提取，通常有 LLM 辅助）到图数据库（Neo4j、Memgraph）。
2. **查询图谱**：用户问题被解析为实体；查询图谱获取相关实体和关系；检索的图数据增强向量检索。
3. **组合**：向量检索给非结构化上下文；图检索给结构化上下文。两者进入 LLM 的 prompt。

KG-RAG 在有强实体-关系结构的领域上闪耀：企业知识库（组织图、产品关系）；医学（药物-药物交互、病症-治疗关系）；法律（案例-引用图）。

它也工程量大。构建和维护知识图谱是大量子项目。大多数生产 RAG 系统 _不_ 使用 KG-RAG；该模式在领域价值特别在于结构化关系时合适。2026 年教训：**当关系是答案时 KG-RAG 是正确模式；当文本是答案时纯向量 RAG 是正确模式**。

Strata Research 考虑了 KG-RAG（案例-引用图结构丰富）最终在 V1–V4 中决定不采用：图谱的价值低于工程成本。他们每季度重新审视决策；如果法律语料库增长超过引用网络分析成为明确功能需求的阈值，KG-RAG 可能进入架构。

### 11.4 绑定工作流 #5：多轴 RAG eval 量表

生产 RAG 评估需要同时测量检索质量和回答质量，跨多轴。绑定工作流是 Strata Research 部署的量表和支撑它的人工标注 SOP。
