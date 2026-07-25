(b) **每功能日成本**：同 (a) 但 `GROUP BY DATE(t.created_at), t.feature_name`。仪表板渲染两个视图；团队用租户视图做计费和客户治理，功能视图做工程投资决策。

(c) **每功能缓存命中率**（仅适用于缓存适用的 Anthropic 路由流量）：


    SELECT
      t.feature_name,
      SUM(t.cached_tokens) / NULLIF(SUM(t.input_tokens), 0) AS cache_hit_rate
    FROM traces t
    WHERE t.model LIKE 'anthropic/%'
      AND t.created_at >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY t.feature_name
    ORDER BY cache_hit_rate DESC;


缓存命中率接近 0 的功能有配置错误的 cache_control 标记或极其多变的 prompt。仪表板浮现这些供调查。

(d) **激增检测查询**（今日 vs 每租户尾部 7 天均值）：


    WITH today AS (
      SELECT tenant_id, SUM(...) AS cost_today  -- 同 (a) 的成本表达式
      FROM traces
      WHERE DATE(created_at) = CURRENT_DATE
      GROUP BY tenant_id
    ),
    baseline AS (
      SELECT tenant_id, AVG(daily_cost) AS avg_cost, STDDEV(daily_cost) AS stddev_cost
      FROM (
        SELECT tenant_id, DATE(created_at) AS d, SUM(...) AS daily_cost
        FROM traces
        WHERE created_at BETWEEN CURRENT_DATE - INTERVAL '8 days' AND CURRENT_DATE - INTERVAL '1 day'
        GROUP BY tenant_id, DATE(created_at)
      ) sub
      GROUP BY tenant_id
    )
    SELECT
      t.tenant_id,
      t.cost_today,
      b.avg_cost,
      b.stddev_cost,
      (t.cost_today - b.avg_cost) / NULLIF(b.stddev_cost, 0) AS z_score
    FROM today t
    JOIN baseline b ON t.tenant_id = b.tenant_id
    WHERE (t.cost_today - b.avg_cost) / NULLIF(b.stddev_cost, 0) > 3
    ORDER BY z_score DESC;


z 分数超过 3 触发激增告警。阈值校准到你的噪声水平；日间方差低的团队可用 z>2；突发流量的团队可能需 z>4。

运维笔记：

* 每 15 分钟运行激增检测查询；告警路由到成本值班。
* 成本表达式跨查询重复；封装在 SQL 视图（`call_costs`）中使仪表板和检测器共享一个定义。
* 季度验证：将仪表板总量与提供商发票比较。差异 >2% 表示要么遗漏追踪（插桩缺口）要么定价表过时（提供商改了价格）。

仪表板构建在追踪存储之上，非旁边。添加新仪表板维度（按区域、按客户细分、按 prompt 版本）只是在追踪中加标签和在仪表板加查询；无需新流水线。这是在可观测性上构建成本而非分别构建两者的架构回报。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_给定带[这些字段]的 Langfuse 追踪，编写 SQL 查询：每租户日成本、每功能成本、缓存命中率、带 z 分数的租户成本激增检测器。_ 你验证 (a) 成本公式正确处理缓存 token 按缓存费率（LLM 可能按全费率收缓存 token），以及 (b) 激增检测器使用稳健统计量（滚动窗口上的 z 分数是合理的；固定百分比阈值可能遗漏高方差租户）。
