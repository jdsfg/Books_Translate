### 22.5 推理引擎与托管自托管

如你自托管，2026 年栈：

**推理引擎**（在你的硬件上服务模型的软件）：

* **vLLM**：开源；高吞吐；支持多种架构；自托管生产推理的默认选择。PagedAttention 实现高效内存使用。
* **TGI（Text Generation Inference）**：HuggingFace 的推理引擎；成熟；良好的生态集成。

这些是你会安装在你的 GPU 上的引擎。

**托管自托管平台**（提供 GPU + 推理引擎作为服务）：

* **Modal**：无服务器 GPU 计算；按调用付费；适合可变工作负载。
* **Together AI**：开放权重模型的托管推理；按 token 计费类似 API 提供商但面向开放权重选择。
* **Anyscale**：基于 Ray；为大规模分布式推理设计。
* **Replicate**：托管开放权重模型的简单 API；适合原型。

已出现的分野：托管平台（Together、Replicate）面向想要开放权重但不愿运行基础设施的团队；自托管 vLLM 面向有运维能力且想要最大控制和成本优化的团队。

对 Beacon Health AI 的 HIPAA 约束用例，托管和非托管托管选项通常不可接受；Beacon 要么使用带 BAA 的托管 API 要么内部运行 vLLM。数据敏感性维度比成本更驱动选择。
