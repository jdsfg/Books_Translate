#### 应用题

**Q1.** _设计工具目录_。Beacon Health AI CodeReview Bot 需要工具。设计 agent 在代码审查期间可能使用的 5-7 个工具。指定每个工具的 schema、策略门控（如有）和示例用法。

提示

代码审查涉及：读代码、查历史、查风格指南、发评论。读 vs 写区别重要。

**答案：**

1. **read_file**：


    description: 读取 diff 中特定路径的文件内容。
    input_schema:
      path: string（必须在 PR 的变更文件中；pattern 强制）
      start_line: integer（可选；默认 1）
      end_line: integer（可选；默认文件末尾）
    policy_gating: 无（只读；限制到 PR 的变更文件）


2. **search_codebase**：


    description: 搜索代码库中的符号定义、引用或文本匹配。
    input_schema:
      query: string
      search_type: enum [symbol_definition, symbol_reference, text]
      language: enum [python, go, typescript]（可选）
    policy_gating: 速率限制（每次审查最多 20 次搜索）


3. **get_file_history**：


    description: 获取特定行范围的 git blame 历史，显示代码最后修改时间和修改者。
    input_schema:
      path: string
      start_line: integer
      end_line: integer
    policy_gating: 无（只读）


4. **lookup_style_guide**：


    description: 查找团队特定主题的风格指南（例如"错误处理"、"日志"、"代码中的 PHI"）。
    input_schema:
      topic: string
    policy_gating: 无（只读）


5. **check_security_pattern**：


    description: 对照已知安全反模式检查代码片段（硬编码凭证、日志中的 PHI、不安全反序列化）。
    input_schema:
      code_snippet: string
    policy_gating: 无（确定性检查；高置信度；安全运行）


6. **post_comment**（操作工具）：


    description: 在 PR 的特定行发布审查评论。
    input_schema:
      path: string
      line: integer
      severity: enum [critical, major, minor, informational]
      body: string（最多 1000 字符）
      category: enum [security, style, correctness, performance, documentation]
    policy_gating:
      - 速率限制（每 PR 最多 30 条评论）
      - 确认：agent 必须包含简短理由
      - 内容过滤：评论正文中无 PHI（确定性检查）


7. **flag_for_human_review**（升级工具）：


    description: 当 agent 不确定或检测到高风险变更时将 PR 标记为人工审查。
    input_schema:
      reason: string
      severity: enum [routine_uncertainty, security_concern, scope_too_large]
    policy_gating: 无（升级始终允许）


示例轨迹：bot 读取 PR 的变更文件（read_file），搜索相关代码（search_codebase），查找团队的日志约定（lookup_style_guide），运行安全模式检查（check_security_pattern），并在发现问题上发布评论（post_comment）。对于异常变更模式，标记人工审查（flag_for_human_review）。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？
