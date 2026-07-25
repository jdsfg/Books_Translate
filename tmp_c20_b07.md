剩余分支覆盖 §19.4 schema 中的其他两个 PHI 面：模型响应（字典或原始字符串）和工具调用参数字典。最终 `sink.write` 将脱敏副本发送到不受限存储：

            # `response` 按 §19.4 schema 是字典；遍历其字符串字段。
            if isinstance(span.get("response"), dict):
                for k, v in span["response"].items():
                    if isinstance(v, str):
                        span["response"][k] = redact_phi(v)
            elif isinstance(span.get("response"), str):
                span["response"] = redact_phi(span["response"])
            # 追踪 schema (§19.4)：工具调用 span 有 `type == "tool_call"`
            # 且 `args` 作为 span 本身的顶层字典。
            if span.get("type") == "tool_call" and span.get("args"):
                for k, v in span["args"].items():
                    if isinstance(v, str):
                        span["args"][k] = redact_phi(v)
        sink.write(trace_copy)


**结构性脱敏**：某些字段始终从主存储中存储的追踪中省略（如完整患者图表）。仅保留脱敏摘要或结构性元数据。

**分层访问**：即使在团队内，对含 PHI 的追踪的访问也受限。工程师可自由查看脱敏追踪；未脱敏追踪需显式访问请求并带审计日志。

脱敏模式很重要。基于 NER 的脱敏（使用训练的 PHI 检测器）比正则更全面但更贵且有自身假阴性率。2026 年最佳实践：分层，正则捕获明显案例；NER 捕获长尾；定期审计验证脱敏质量。

**权衡**：脱敏降低调试保真度。调试临床摘要器问题的工程师看到 `[NAME]` 而非"Mr. Smith"；特定身份丢失。这对常规调试通常可接受；对深入调查，团队可通过适当协议请求未脱敏访问。


#### 脱敏是纵深防御，非银弹

团队有时将脱敏视为 _消除_ HIPAA 关注。它不是。脱敏的 PHI 在某些解释下仍是 PHI——通过临床上下文重新识别是可能的——所以脱敏减少表面积而不退役监管负担。HIPAA 合规基础设施仍需要；脱敏是纵深防御的一层。将其读为银弹导致对必须在其后的监管架构投资不足。
