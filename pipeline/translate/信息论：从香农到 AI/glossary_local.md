# 本地术语库：信息论：从香农到 AI（glossary_local）

> 本书工作目录专用。与共享库 glossary_ml_data.md 并用：命中共享库用共享译法，命中本地库用本地译法。
> 格式：英文原名 | 中文标准名 | 备注

## 核心量与定义
self-information | 自信息 |
surprise | 惊异 | self-information 的直觉同义词
Shannon entropy | 香农熵 |
binary entropy function | 二元熵函数 | H_b(p)
joint entropy | 联合熵 |
conditional entropy | 条件熵 |
differential entropy | 微分熵 | 连续型；信息论惯例译"微分熵"
relative entropy | 相对熵 | 即 KL 散度
cross-entropy | 交叉熵 |
entropy rate | 熵率 |
redundancy | 冗余 |
perplexity | 困惑度 |

## 定理 / 不等式 / 性质
chain rule | 链式法则 |
Jensen's inequality | 詹森不等式 |
Gibbs' inequality | 吉布斯不等式 |
Fano's inequality | 法诺不等式 |
Kraft inequality | 克拉夫特不等式 |
data processing inequality | 数据处理不等式 | DPI
asymptotic equipartition property | 渐近均分性 | AEP，首现注 AEP
typical set | 典型集 |
source coding theorem | 信源编码定理 |
channel coding theorem | 信道编码定理 |
noisy-channel coding theorem | 有噪信道编码定理 |
rate-distortion theory | 率失真理论 |
rate-distortion function | 率失真函数 |
information bottleneck | 信息瓶颈 | IB
maximum entropy | 最大熵 |
concavity | 凹性 |
convexity | 凸性 |

## 编码
source coding | 信源编码 |
channel coding | 信道编码 |
lossless compression | 无损压缩 |
lossy compression | 有损压缩 |
prefix code | 前缀码 |
prefix-free code | 无前缀码 |
Huffman coding | 霍夫曼编码 |
arithmetic coding | 算术编码 |
Shannon-Fano coding | 香农-法诺编码 |
Lempel-Ziv | Lempel-Ziv | 保留原名
codeword | 码字 |
codebook | 码本 |
block code | 分组码 |
error-correcting code | 纠错码 |
Hamming code | 汉明码 |
LDPC | LDPC | 低密度奇偶校验码，保留缩写
turbo code | Turbo 码 |
parity check | 奇偶校验 |

## 信道 / 容量
channel capacity | 信道容量 |
binary symmetric channel | 二元对称信道 | BSC
binary erasure channel | 二元擦除信道 | BEC
noise | 噪声 |
signal-to-noise ratio | 信噪比 | SNR
Gaussian channel | 高斯信道 |
water-filling | 注水 | 注水算法/注水定理

## 散度 / 几何 / 变分
KL divergence | KL 散度 |
Kullback-Leibler | 库尔贝克-莱布勒 |
Jensen-Shannon divergence | JS 散度 |
f-divergence | f-散度 |
Bregman divergence | 布雷格曼散度 |
Wasserstein distance | Wasserstein 距离 | 保留原名
information geometry | 信息几何 |
Fisher information | 费舍尔信息 |
natural gradient | 自然梯度 |
variational methods | 变分方法 |
variational inference | 变分推断 |
evidence lower bound | 证据下界 | ELBO，首现注 ELBO
variational autoencoder | 变分自编码器 | VAE
reparameterization trick | 重参数化技巧 |

## 现代 AI 关联
compression-prediction equivalence | 压缩-预测等价 |
language model | 语言模型 | LM
token | 词元 | 首现注 token，可正文用 token
bits per token | 每词元比特数 | bits per token
bits per character | 每字符比特数 | bits per character
transformer | Transformer | 保留原名
attention | 注意力 |
deep learning | 深度学习 |
neural network | 神经网络 |
classifier | 分类器 |
generative model | 生成模型 |
one-hot | 独热 | one-hot 向量
logits | logits | 保留原名
softmax | softmax | 保留原名
mutual information estimator | 互信息估计量 |
InfoNCE | InfoNCE | 保留原名
lower bound | 下界 |
upper bound | 上界 |

## 概率 / 统计基础
random variable | 随机变量 |
probability mass function | 概率质量函数 | PMF
probability density function | 概率密度函数 | PDF
Markov chain | 马尔可夫链 |
stationary | 平稳 |
i.i.d. | 独立同分布 | i.i.d.
expectation | 期望 |
estimator | 估计量 |
prior | 先验 |
posterior | 后验 |
likelihood | 似然 |

## 量子信息
quantum information | 量子信息 |
von Neumann entropy | 冯·诺伊曼熵 |
qubit | 量子比特 |
density matrix | 密度矩阵 |
entanglement | 纠缠 |

## 人名（首现可保留英文，中文统一）
Shannon | 香农 | Claude Shannon
Hartley | 哈特利 |
Khinchin | 辛钦 |
Huffman | 霍夫曼 |
Kraft | 克拉夫特 |
Fano | 法诺 |
Kolmogorov | 柯尔莫哥洛夫 |
Tishby | Tishby | 保留原名（信息瓶颈）
Saxe | Saxe | 保留原名
McAllester | McAllester | 保留原名
Stratos | Stratos | 保留原名
Slepian-Wolf | Slepian-Wolf | 保留原名
von Neumann | 冯·诺伊曼 |

---

_本地术语库，翻译过程中随现随补（回填）。共享库只读，不追加。_
