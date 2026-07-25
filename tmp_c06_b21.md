**Q5.** _设计 eval 存储 schema_。实现概念检查 Q5 和 §5.4 引用的 SQLite schema。指定支持以下功能所需的表、列、索引和外键关系：(a) 每运行聚合分数；(b) 每案例每维度分数；(c) prompt 版本跟踪；(d) 数据集版本跟踪；(e) CI 工作流使用的"获取分支 X 在提交 Y 的基线"查询。同时指出一个经常让团队绊倒的 schema 决策。

提示

四张表足够：`runs`、`case_scores`、`prompts`、`datasets`。外键连接它们。CI 基线查询需要在 `runs` 上 (branch, commit_sha) 的索引。

**答案：** Schema：


    CREATE TABLE prompts (
        id INTEGER PRIMARY KEY,
        version TEXT NOT NULL UNIQUE,         -- 例如 "summarizer/1.4.0"
        content_sha TEXT NOT NULL,            -- prompt 文本的 sha256
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        author TEXT NOT NULL,                 -- 注册此版本的工程师
        description TEXT
    );

    CREATE TABLE datasets (
        id INTEGER PRIMARY KEY,
        version TEXT NOT NULL UNIQUE,         -- 例如 "clinical_triage_v3"
        case_count INTEGER NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    );

    CREATE TABLE runs (
        id INTEGER PRIMARY KEY,
        prompt_id INTEGER NOT NULL REFERENCES prompts(id),
        dataset_id INTEGER NOT NULL REFERENCES datasets(id),
        branch TEXT NOT NULL,                 -- "main", "feature/foo"
        commit_sha TEXT NOT NULL,
        triggered_by TEXT NOT NULL,           -- "ci", "manual", "nightly"
        started_at TEXT NOT NULL,
        finished_at TEXT,
        summary_score REAL,                   -- 聚合，完成时填充
        status TEXT NOT NULL DEFAULT 'running' -- 'running','complete','failed'
    );

    CREATE INDEX idx_runs_branch_commit ON runs(branch, commit_sha);
    CREATE INDEX idx_runs_prompt_dataset ON runs(prompt_id, dataset_id);
    CREATE INDEX idx_runs_started_at ON runs(started_at);

    CREATE TABLE case_scores (
        id INTEGER PRIMARY KEY,
        run_id INTEGER NOT NULL REFERENCES runs(id),
        case_id TEXT NOT NULL,                -- golden set 案例标识符
        dimension TEXT NOT NULL,              -- "clinical_accuracy", "completeness" 等
        score REAL NOT NULL,
        metadata_json TEXT                    -- 每案例评判者备注、延迟、token
    );

    CREATE INDEX idx_case_scores_run ON case_scores(run_id);
    CREATE INDEX idx_case_scores_case_dim ON case_scores(case_id, dimension);


CI 使用的基线查找查询：


    SELECT r.id, r.summary_score, r.commit_sha
    FROM runs r
    WHERE r.branch = 'main'
      AND r.status = 'complete'
      AND r.prompt_id = (SELECT id FROM prompts WHERE version = ?)
      AND r.dataset_id = (SELECT id FROM datasets WHERE version = ?)
    ORDER BY r.started_at DESC
    LIMIT 1;


(branch, commit_sha) 上的索引加速按提交查找；(prompt_id, dataset_id) 上的索引加速此 prompt 和数据集的最新基线查询。两者都需要。
