### 5.4 SQLite 支持的 eval 存储：一个小而强大的组件

Aiyana 在 Beacon Health AI 的选择是使用 `pytest-evals` 作为运行器和一个小型 SQLite 存储用于 eval 结果历史。存储是二十行 Python；它做了超比例的工作。

Schema：


    CREATE TABLE eval_runs (
        run_id TEXT PRIMARY KEY,
        git_sha TEXT NOT NULL,
        prompt_version TEXT NOT NULL,
        model_version TEXT NOT NULL,
        started_at TIMESTAMP NOT NULL,
        finished_at TIMESTAMP,
        total_cases INTEGER NOT NULL,
        summary_score REAL
    );

    CREATE TABLE eval_cases (
        run_id TEXT NOT NULL,
        case_id TEXT NOT NULL,
        scores_json TEXT NOT NULL,
        output_text TEXT,
        PRIMARY KEY (run_id, case_id),
        FOREIGN KEY (run_id) REFERENCES eval_runs(run_id)
    );

    CREATE INDEX idx_runs_git_sha ON eval_runs(git_sha);
    CREATE INDEX idx_runs_prompt ON eval_runs(prompt_version);


这就是整个数据模型。两张表；一个外键；两个索引。每次 eval 运行产生一行 `eval_runs` 和 N 行 `eval_cases`。一个每夜脚本跨运行聚合摘要统计。一个小型 Python CLI 查询存储进行 delta 分析（"显示提交 X 和提交 Y 之间 clinical_summary 套件的分数变化"）。

存储是仓库或共享内部服务本地的；它不去 SaaS 供应商；它不携带 PHI（因为 eval 集是合成 PHI）。存储也跨年持久：Beacon 某办公室的一个 SQLite 文件包含自功能上线以来临床笔记摘要器的每个 eval 结果。审计跟踪、回归检测、模型升级比较，全部来自 200 行技术栈。

**为什么是 SQLite。** 它是单文件。它不需要服务器。它在版本控制检查中存活（一个在未检入的 `data/` 目录中的二进制文件，带定期备份）。它扩展到即使激进团队一年也会产生的数百万 eval 案例行。当团队最终超出 SQLite 时，迁移到 Postgres 是直接的；在那之前，最简单的工具获胜。
