### 3.2 Streaming：它是什么以及何时使用

默认情况下，chat-completions 调用保持连接打开直到模型完成生成，然后返回整个响应。对于 500 token 的输出按每秒 50 token，那是用户看到任何内容之前 10 秒的等待。对于交互式 UI，这是不可接受的。

Streaming 改变了交付模型。API 不等待完整响应，而是返回一个 server-sent events (SSE) 流，每个事件包含生成过程中输出的一部分。客户端将每部分追加到显示缓冲区；用户看到文本逐 token 出现，就像 ChatGPT 的样子。完成的总挂钟时间相同；_首 token 时间_（TTFT）在 2026 年降至通常 200–600 毫秒，对用户来说感觉是即时的。

    with client.messages.stream(
        model="claude-sonnet-4-20260315",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Explain RAG in two paragraphs."}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        final = stream.get_final_message()


几个实际注意事项：

1. **Streaming 改变你的错误处理。** 非流式调用要么完全成功要么完全失败。流式调用可能前 200 token 成功，然后因服务器错误失败，留给客户端一个部分响应。你的代码必须决定如何处理部分输出（带错误标记显示？丢弃？保存供重试？）。
2. **Streaming 改变你的用量统计。** 使用 streaming，`usage` 字段在流的末尾通过最终的 `message_stop` 事件传递。直接从非流式响应读取 `response.usage` 的代码必须适配为读取流的最终消息。
3. **Streaming 对交互式 UI 必不可少；对批处理无用。** 一个总结 10,000 个文档并将结果写入数据库的后端任务不需要 streaming；数据库不关心 TTFT。将复杂性留给重要的场景。
4. **Streaming 对语音必不可少。** 低于 500 毫秒的 TTFT 预算（第 20 章）不使用 streaming 无法满足。语音管道在前几个 token 上开始语音合成，与模型继续生成并行。
