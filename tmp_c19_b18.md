**Q4.** _审计工作负载批量合格性_。列出 SaaS 公司的五个常见 AI 工作负载。对每个，识别是否批量合格及切换的工程工作。

**答案：**

1. **实时聊天助手**（同步面向用户）。非批量合格。用户等待响应；延迟预算亚秒。保持实时。

2. **文档摄取 / 重新索引**。批量合格。用户不等待索引完成；文档在批量完成后可搜索。工程工作：将 API 客户端切换到批量端点；添加状态追踪流水线（作业可耗时分钟到小时）。约 1 工程师周。

3. **夜间摘要报告生成**。批量合格。报告隔夜生成；用户早上看到。工程工作：重新架构作业以提交批量作业并轮询完成。约 1-2 工程师周。

4. **Eval 套件运行**。大部分批量合格。对 1000 golden 案例在候选 prompt 上运行 eval；团队等一小时或隔夜运行。工程工作：更新 pytest-evals（或你的 eval 运行器）使用批量 API。约 1 工程师周。

5. **客户入职 AI 欢迎消息**。大部分实时（客户期望注册时立即欢迎）。可部分批量（为预测注册预先生成欢迎），但对大多数团队工程复杂度超过节省。保持实时。

大多数生产团队的审计揭示 30-60% 推理量是批量合格的；切换捕获该部分 50% 折扣。工程工作相对于节省小。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_对这 5 个工作负载，确定批量合格性并估算切换工程量。_ 你验证 (a) LLM 正确识别 _用户等待_ 维度（用户等待的工作负载无论节省多诱人都不批量合格），以及 (b) 工程量估算现实（LLM 有时低估；对照你团队速度检查）。

**Q5.** _从可观测性追踪构建成本仪表板_。你的团队用 Langfuse 做追踪。每个追踪已包含：tenant_id、feature_name、model、input_tokens、output_tokens、cached_tokens、latency_ms、eval_score（评分时）。设计从追踪存储产生 §18.8 成本仪表板的 SQL（或等价）查询。指定：(a) 每租户日成本；(b) 每功能日成本；(c) 每功能缓存命中率；(d) 激增检测查询。

提示

每 100 万 token 价格因模型而异。成本公式需要连接每 token 成本表。缓存 token 按折扣费率计算。

**答案：**

假设 `model_pricing` 表有 `model, input_per_1m, cached_per_1m, output_per_1m`。

(a) **每租户日成本**：


    SELECT
      DATE(t.created_at) AS day,
      t.tenant_id,
      SUM(
        (t.input_tokens - COALESCE(t.cached_tokens, 0)) * mp.input_per_1m / 1e6
        + COALESCE(t.cached_tokens, 0) * mp.cached_per_1m / 1e6
        + t.output_tokens * mp.output_per_1m / 1e6
      ) AS cost_usd,
      COUNT(*) AS call_count
    FROM traces t
    JOIN model_pricing mp ON t.model = mp.model
    WHERE t.created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 1, 2
    ORDER BY day DESC, cost_usd DESC;
