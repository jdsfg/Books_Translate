# 风格简报 · CS 系统系列（db_systems / comp_nets / os_book / dist_sys / sys_design / debug_think / swe_craft）

> 覆盖：数据库系统 / 计算机网络 / 操作系统 / 分布式系统 / 系统设计思维 / 调试思维 / 软件工程匠艺。技术/工程书，**质量 bar = 准确 + 通顺 + 领域惯例**。

## 1. 系列定位
计算机系统（DB / 网络 / OS / 分布式 / 架构 / 调试 / 软工）。硬核技术，概念密集，常含代码、时序、协议。

## 2. 质量 bar（核心）
- **准确优先**：协议、算法、数据结构、API 语义零容错。
- **领域惯例**：被动语态可保留；代码注释照译；伪代码/时序原样。
- **克制**：不润色成散文，技术陈述求精确。

## 3. 人称 / 语气
- 中性陈述；示例用"我们"可保留。
- 不替作者下原书没有的架构判断。

## 4. 术语处理（关键）
- 首现加注原文：throughput（吞吐）、latency（延迟）、concurrency（并发）、idempotent（幂等）、consensus（共识）、replication（复制）、partition（分区）、deadlock（死锁）、race condition（竞态）、syscall（系统调用）、kernel（内核）、scheduler（调度器）、cache（缓存）、index（索引）、transaction（事务）、ACID、CAP。
- 协议/标准名保留英文（TCP、Raft、Paxos、SQL）。

## 5. 禁忌译法
- training 在此系列不出现；若出现于 ML 交叉内容按 AI Science 规则（训练）。
- transaction = 事务（DB 语境），非"交易"。
- process / thread = 进程 / 线程，不混用。
- 不把英文缩写（e.g. RPC）展开成中文再译。

## 6. 结构保全
- 代码块、命令行、表格、公式、脚注、标题层级原样。
- 协议图、时序图注保留。

## 7. 数字规则（强制阿拉伯 + 原单位）
- 端口（:8080）、延迟（12 ms）、吞吐（1.2M req/s）、副本数（3 副本）、超时（30 s）、QPS 一律阿拉伯 + 原单位。
- 版本号（HTTP/2、TLS 1.3）原样。

## 8. 示例
- 源：`A deadlock occurs when two transactions wait on each other's locks.`
- 译：`当两个事务互相等待对方持有的锁时，就会发生死锁（deadlock）。`
- 源：`The system targets 99.95% availability with 3 replicas.`
- 译：`系统以 3 个副本实现 99.95% 的可用性目标。`

---

_最后更新：2026-07-19。技术系列记"精度与惯例"；数字强制阿拉伯+原单位。_
