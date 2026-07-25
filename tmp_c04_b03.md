#### 定义：Role

附加到对话中每条消息的标签，告诉模型如何对待它。三种角色占主导：`system`（来自开发者的指令，被视为特权）；`user`（与模型对话的人类或上游系统）；`assistant`（模型之前的回答，当你想让它继续或引用自己早期输出时回显）。

用大白话说：role 是你告诉模型 _谁在说话_ 的方式。模型被训练（按 §2.3）将 system 角色内容视为权威配置，user 角色内容视为要处理的输入，assistant 角色内容视为自己之前的发言。角色分离是多轮对话的基础，也是防御 prompt 注入的第一道防线（第 23 章）。

#### 最小多轮请求

一个带 system prompt 和对话历史的真实调用：


    response = client.messages.create(
        model="claude-sonnet-4-20260315",
        max_tokens=1024,
        system="You are a code reviewer for Beacon Health AI. Be concise. Flag security iss
ues with priority. Do not invent file names that are not in the diff.",                            messages=[
            {"role": "user", "content": "Review this diff:\n```python\nimport os\nDB_PASSWO
RD = 'changeme'\n```"},                                                                                {"role": "assistant", "content": "Security issue: hard-coded password 'changeme
' is a placeholder credential committed to source. Move to environment variable; document t
he expected variable name in the README."},                                                            {"role": "user", "content": "What variable name do you suggest?"},
        ],
        temperature=0,
    )


这是你余生将与之工作的结构。注意固定的模型版本、显式的 `max_tokens`、给模型角色和硬约束的 system prompt，以及 `temperature=0` 用于代码审查任务的可复现性——你不希望创造力。
