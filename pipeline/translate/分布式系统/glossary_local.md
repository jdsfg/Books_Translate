# 分布式系统 术语表

| 英文 | 中文 |
|---|---|
| distributed system | 分布式系统 |
| CAP theorem | CAP 定理 |
| PACELC | PACELC（保留英文） |
| consistency | 一致性 |
| availability | 可用性 |
| partition tolerance | 分区容错性 |
| latency | 延迟 |
| consensus | 共识 |
| Paxos | Paxos（保留英文） |
| Raft | Raft（保留英文） |
| replication | 复制 |
| replica | 副本 |
| sharding | 分片 |
| partitioning | 分区 |
| resharding | 重分片 |
| eventual consistency | 最终一致性 |
| strong consistency | 强一致性 |
| causal consistency | 因果一致性 |
| linearizability | 线性一致性 |
| serializability | 串行化 |
| atomicity | 原子性 |
| idempotency | 幂等性 |
| exactly-once semantics |  exactly-once 语义 / 恰好一次语义 |
| at-least-once | at-least-once / 至少一次 |
| at-most-once | at-most-once / 至多一次 |
| two-phase commit | 两阶段提交 |
| 2PC | 2PC（保留英文） |
| three-phase commit | 三阶段提交 |
| 3PC | 3PC（保留英文） |
| CRDT | CRDT（保留英文） |
| snapshot | 快照 |
| leader election | 领导者选举 |
| failover | 故障转移 |
| fault tolerance | 容错 |
| byzantine fault | 拜占庭故障 |
| Byzantine fault tolerance | 拜占庭容错 |
| cascading failure | 级联故障 |
| retry storm | 重试风暴 |
| metastable failure | 亚稳态故障 |
| gray failure | 灰色故障 |
| chaos engineering | 混沌工程 |
| load balancing | 负载均衡 |
| speculative decoding | 投机解码 |
| KV cache | KV 缓存 |
| vLLM | vLLM（保留英文） |
| SGLang | SGLang（保留英文） |
| distributed tracing | 分布式追踪 |
| service discovery | 服务发现 |
| configuration management | 配置管理 |
| distributed lock | 分布式锁 |
| cache coherence | 缓存一致性 |
| gossip protocol | gossip 协议 / 流言协议 |
| vector clock | 向量时钟 |
| logical clock | 逻辑时钟 |
| physical clock | 物理时钟 |
| monotonic clock | 单调时钟 |
| quorum | 法定人数 |
| majority quorum | 多数法定人数 |
| flexible quorum | 灵活法定人数 |
| lease | 租约 |
| fencing token | 围栏 token |
| backpressure | 背压 |
| circuit breaker | 断路器 |
| bulkhead | 舱壁 |
| timeout | 超时 |
| retry | 重试 |
| jitter | 抖动 |
| exponential backoff | 指数退避 |
| rate limiter | 限流器 |
| LSM tree | LSM 树 |
| write-ahead log | 预写日志（WAL） |
| WAL | WAL（保留英文） |
| consensus protocol | 共识协议 |
| state machine replication | 状态机复制 |
| primary-backup replication | 主备复制 |
| multi-leader replication | 多主复制 |
| leaderless replication | 无主复制 |
| read repair | 读修复 |
| hinted handoff | 提示移交 |
| anti-entropy | 反熵 |
| Merkle tree | Merkle 树 |
| bloom filter | 布隆过滤器 |
| consistent hashing | 一致性哈希 |
| virtual node | 虚拟节点 |
| token bucket | 令牌桶 |
| sliding window | 滑动窗口 |
| distributed transaction | 分布式事务 |
| sagas | sagas（保留英文） |
| outbox pattern | 发件箱模式 |
| idempotent consumer | 幂等消费者 |
| message broker | 消息代理 |
| publish-subscribe | 发布-订阅 |
| event sourcing | 事件溯源 |
| command query responsibility segregation | CQRS（命令查询职责分离） |
| CQRS | CQRS（保留英文） |
| consensus group | 共识组 |
| log replication | 日志复制 |
| term | 任期 |
| log entry | 日志条目 |
| commit index | 提交索引 |
| last applied | 最后应用 |
| match index | 匹配索引 |
| next index | 下一索引 |
| split brain | 脑裂 |
| network partition | 网络分区 |
| clock skew | 时钟偏移 |
| clock drift | 时钟漂移 |
| happens-before | happens-before / 发生于之前 |
| causal broadcast | 因果广播 |
| atomic broadcast | 原子广播 |
| reliable broadcast | 可靠广播 |
| total order broadcast | 全序广播 |
| FIFO broadcast | FIFO 广播 |
| causal order | 因果序 |
| total order | 全序 |
| partial order | 偏序 |
| distributed deadlock | 分布式死锁 |
| liveness | 活性 |
| safety | 安全性 |
| determinism | 确定性 |
| nondeterminism | 非确定性 |
| model checking | 模型检测 |
| TLA+ | TLA+（保留英文） |
| formal verification | 形式化验证 |
| correctness | 正确性 |
| performance | 性能 |
| throughput | 吞吐 |
| tail latency | 尾部延迟 |
| percentile | 百分位 |
| p99 latency | p99 延迟 |
| horizontal scaling | 水平扩展 |
| vertical scaling | 垂直扩展 |
| elasticity | 弹性 |
| autoscaling | 自动扩缩容 |
| multi-tenancy | 多租户 |
| single point of failure | 单点故障 |
| mean time to recovery | 平均恢复时间（MTTR） |
| mean time between failures | 平均故障间隔时间（MTBF） |
| service level objective | 服务等级目标（SLO） |
| service level agreement | 服务等级协议（SLA） |
| service level indicator | 服务等级指标（SLI） |
| observability | 可观测性 |
| telemetry | 遥测 |
| metric | 指标 |
| log | 日志 |
| trace | 追踪 |
| span | 跨度 |
| NVIDIA NIM | NVIDIA NIM（保留英文） |
| prefill/decode disaggregation | prefill/decode 分离 |
| continuous batching | continuous batching / 连续批处理 |
| paged attention | paged attention / 分页注意力 |
| tensor parallelism | tensor parallelism / 张量并行 |
| pipeline parallelism | pipeline parallelism / 流水线并行 |
| data parallelism | data parallelism / 数据并行 |
| expert parallelism | expert parallelism / 专家并行 |
| sequence parallelism | sequence parallelism / 序列并行 |
| model parallelism | model parallelism / 模型并行 |
