# 风格简报 · ML / 数据 / 复杂性系列（ml_book / info_theory / stat_thinking / complexity_sci）

> 覆盖：机器学习：从数据到智能 / 信息论：从香农到 AI / AI时代的统计思维 / 复杂性科学入门。
> **本简报被 P0 前三本（信息论 / 复杂性科学 / AI 统计思维）共用，务必写厚。** 技术/科学书，**质量 bar = 准确 + 通顺 + 领域惯例**，内容精度 > 文采。

## 1. 系列定位
横跨 ML、信息论、统计、复杂性科学。数学与概念密集，含大量公式、定义、概率/信息度量。受众有理科背景。

## 2. 质量 bar（核心）
- **准确优先**：公式、符号、定理、数值、定义零容错（这是 P0 大书，错一处连锁歪）。
- **领域惯例**：被动语态可保留；公式/符号原样不译；定义陈述精确。
- **通顺但克制**：长推导可分段，但逻辑链不断。

## 3. 人称 / 语气
- 中性陈述；教学式"我们不妨"可保留。
- 不替作者补最新研究（避免时效错位）。

## 4. 术语处理（关键，分域）
- **ML**：gradient（梯度）、loss（损失）、epoch（轮）、batch（批次）、overfitting（过拟合）、regularization（正则化）、embedding（嵌入）、activation（激活）。
- **信息论**：entropy（熵）、mutual information（互信息）、bit（比特）、nats、channel capacity（信道容量）、KL divergence（KL 散度）、Shannon。
- **统计**：variance（方差）、hypothesis（假设）、p-value（p 值）、regression（回归）、correlation（相关）、Bayesian（贝叶斯）、sample（样本）、confidence interval（置信区间）。
- **复杂性**：emergence（涌现）、attractor（吸引子）、Markov（马尔可夫）、phase transition（相变）、agent-based（基于智能体）、network（网络）、feedback loop（反馈环）。
- 首现加注原文；符号（H(·)、I(X;Y)、σ、μ）原样。

## 5. 禁忌译法
- training = 训练（ML 语境），非"练习"。
- inference = 推理（ML/统计推断语境），非"结论"。
- bit / nats 保留单位，不译"比特/奈特"亦可，但须一致；建议首现注中文后正文用原文单位。
- entropy 在信息论=熵，勿与热力学外行化混。

## 6. 结构保全（重中之重）
- **LaTeX 公式 `$` / `$$` 原样**，绝不改符号或丢失上下标。
- 代码块、表格、脚注、定理/定义框、标题层级原样。
- 数学符号（∑ ∏ ∫ ∈ ∀ ∃）原样。

## 7. 数字规则（强制阿拉伯 + 原单位）
- 百分比（95% CI）、样本量（n=1000）、维度（d=512）、参数（1.5B）、比特（8 bits）、概率（p<0.05）、年份、公式内数字一律阿拉伯 + 原单位。
- 统计/公式数尤须保留（本系列高密）。

## 8. 示例
- 源：`The mutual information I(X;Y) measures dependence.`
- 译：`互信息 I(X;Y) 度量的是依赖程度。`
- 源：`With p < 0.05 we reject the null hypothesis.`
- 译：`当 p < 0.05 时，我们拒绝原假设（null hypothesis）。`
- 源：`Shannon entropy H = -Σ p(x) log p(x) bits.`
- 译：`香农熵 H = -Σ p(x) log p(x)，单位为比特（bits）。`

---

_最后更新：2026-07-19。技术系列记"精度与惯例"；数字强制阿拉伯+原单位；公式/符号零容错（P0 大书共用本简报）。_
