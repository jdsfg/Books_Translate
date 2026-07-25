2. **Postgres 中的 schema 设计。** 每个块成为一行：`(id, source_id, chunk_text, embedding vector(768), metadata jsonb, created_at, updated_at)`。在 `embedding` 上创建 HNSW 索引带适当参数（`m=16, ef_construction=64` 是合理默认）。规划 BM25 层：要么 Postgres tsvector 用于 Postgres 内 BM25，要么单独 BM25 索引（Elasticsearch / OpenSearch）用于更丰富评分。
3. **并行构建 pgvector 索引**同时 Pinecone 在线。从 Pinecone 流式传输嵌入或从源文档重新嵌入。重新嵌入更安全（确保索引从当前真实来源构建，非可能陈旧的 Pinecone 向量）；流式传输更快但继承任何 Pinecone 漂移。
4. **影子 eval pgvector 索引**对照 Pinecone 在样本上（5 到 10% 生产流量）。比较检索质量和延迟。调优良好的 pgvector 应在检索 eval 噪声内与 Pinecone 相当；如不是，切换前调试。
5. **按租户或按功能金丝雀**（同 Q4）。将小部分路由到 pgvector；观察。
6. **渐进推出**在 2 到 4 周内，以质量和延迟观察为门控。
7. **退役 Pinecone**在 100% pgvector 稳定期后。保留 Pinecone 索引可用于短期回滚一个计费周期，然后取消。

**与正向（Q4）的差异：**

* _运维形态变化（从托管到自托管）_。Pinecone 到 pgvector 意味团队承担新运维工作：HNSW 索引调优、向量数据的 Postgres 备份/恢复、vacuum 调优。正向（小到 Pinecone）是 _更少_ 运维；反向是 _更多_ 运维。规划团队容量。
* _混合搜索故事变化_。Pinecone 在托管服务中有原生混合（稀疏向量 + 密集向量）。pgvector 本身无原生 BM25；你用 Postgres tsvector 或外部 BM25 构建。检索架构可能需要新组件；为此预算。
* _元数据过滤性能_。Pinecone 在规模上优化元数据过滤；pgvector 带 JSON 元数据上的 `WHERE` 子句对某些查询模式可能更慢。分析你常见过滤模式；如慢，在常见元数据字段上添加显式 Postgres 索引。
* _成本数学反转_。正向是 _Pinecone 在小规模便宜；pgvector 节省运维_。反向是 _Pinecone 在我们当前规模昂贵；pgvector 几月内回本_。计算盈亏平衡和运维开销附加费；验证迁移自身合理。

**反向迁移特有新风险：**

1. **重新嵌入成本。** 如果嵌入模型自语料库首次摄取到 Pinecone 后已变更（provider 弃用、团队更改嵌入选择），迁移是重新嵌入的机会但也是成本。50M 块语料库按 0.10 美元/M token，约 3K 美元到 5K 美元重新嵌入成本。规划预算。
2. **混合搜索回归。** 如果 Pinecone 的原生混合对你的查询做了真实工作（稀疏向量贡献），迁移到 pgvector 无等价混合设置会回归质量。在切换前构建混合层；用 pgvector 中的完整混合设置做影子 eval。
