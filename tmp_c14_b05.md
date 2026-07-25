### 13.4 工具目录：设计纪律

生产工具目录会增长。团队第一个 agent 有 3 个工具；六个月后有 30 个；一年后有 80 个。增长是有机的（每个客户功能请求成为候选工具），但架构纪律重要。

工具目录设计的三个原则：

**原则 1：工具应该正交。** 每个工具应做一件事。重叠的工具（`get_user` 和 `lookup_user`）混淆模型。捆绑多操作的工具（`do_everything_for_an_order`）变得难以安全使用。

**原则 2：工具应该优雅失败。** 失败的工具（网络错误、无效输入、权限拒绝）应返回模型可读取并反应的结构化错误，而非抛出崩溃应用的异常。模式：

    def execute_tool(name: str, args: dict) -> dict:
        try:
            return {"status": "success", "data": run_tool(name, args)}
        except ToolValidationError as e:
            return {"status": "error", "error_kind": "invalid_input", "message": str(e)}
        except ToolPermissionError as e:
            return {"status": "error", "error_kind": "permission_denied", "message": str(e)}
        except Exception as e:
            return {"status": "error", "error_kind": "internal",
                    "message": "工具失败；尝试不同方法。"}

结构化错误让模型恢复（尝试不同参数、尝试不同工具或优雅放弃）。

**原则 3：危险工具需要显式门控。** 执行破坏性或昂贵操作的工具（退款、删除、发送通知、执行代码）在生产中不应仅由模型可调用。模式：在 LLM 的工具调用决策和执行之间的确定性策略层。对于 Helios 的退款工具：策略层对照租户限制检查金额；将高价值退款路由到人工审批；记录请求；然后才执行。LLM 提议；确定性层处置。

这是第 2 章 §2.11（_用产品混淆模型_）的原则在工具层的应用。模型可以决定调用工具；确定性层执行策略。两者都是安全生产 agent 所需的。
