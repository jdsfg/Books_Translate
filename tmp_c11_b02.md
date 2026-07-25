### 10.2 选择嵌入模型：2026 年格局

2026 年，四个模型家族主导：

**OpenAI `text-embedding-3-small` 和 `text-embedding-3-large`**：通用、良好支持、广泛语言覆盖、有竞争力定价（small 0.02 美元/1M token；large 0.13 美元/1M）。大多数无领域特定需求团队的默认选择。

**Cohere `embed-v3`（英语/多语言）**：强通用性能；多语言变体覆盖 100+ 语言且质量接近单语言；定价与 OpenAI 竞争。非英语或混合语言语料库的好默认。

**Voyage AI**：为特定领域调优的专用嵌入：`voyage-law-2` 用于法律文本、`voyage-code-3` 用于代码、`voyage-finance-2` 用于金融。专用优势是真实的（在目标领域上比通用模型检索 recall 高 3–8 分）但成本略高。

**BGE 系列（开放权重）**：`bge-large-en-v1.5`、`bge-m3` 及后续。开放权重强通用性能；你自托管（vLLM、Triton 等）。成本是你的计算（大规模时常比按 token API 便宜）；运维复杂性是你的。

2026 年决策矩阵：

如果你的语料库是... | 推荐起点
---|---
通用英语内容 | `text-embedding-3-large` 或 `embed-v3-english`
多语言内容 | `embed-v3-multilingual`
领域特定（法律、医学、金融、代码） | 专用（Voyage 或微调 BGE）；先评估
自托管要求（数据隐私） | BGE 系列在你的基础设施上
大规模成本极度敏感 | BGE 自托管；或 `text-embedding-3-small`

Strata Research 在其法律语料库 eval 上评估了 `text-embedding-3-large` vs `voyage-law-2`。结果：text-embedding-3-large 检索 recall@10 为 0.71；voyage-law-2 为 0.79。8 分提升是实质性的，相当于大约两个月的其他工程工作。Strata 采用 voyage-law-2；成本溢价（每次查询约多 30%）相比工程价值很小。

通用规则：**在承诺前在你的特定语料库和查询上评估嵌入**。供应商基准（MTEB、MIRACL）作为相对排序有用但不预测你的特定性能。第 4 章的 eval 纪律适用。
