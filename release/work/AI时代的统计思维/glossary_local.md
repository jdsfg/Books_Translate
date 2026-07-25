# 本书本地术语库：AI时代的统计思维（stat_thinking）

> 仅本书使用，补充共享库 glossary_ml_data.md 未收录/易歧义的统计术语。格式：英文 | 中文 | 备注
> 命中共享库用共享译法；命中本地库用本地译法；两库都无再现译并回填本此。

## 推断与估计
inference | 推断 | 统计语境用"推断"，ML 语境仍作"推理"（见共享库）
statistical inference | 统计推断 |
estimator | 估计量 |
estimate | 估计值 | 名词
estimation | 估计 |
point estimate | 点估计 |
interval estimate | 区间估计 |
bias | 偏差 | 统计偏差，非"偏见"
unbiased | 无偏 |
consistency | 相合性 | 估计量性质
efficiency | 有效性 | 估计量性质
maximum likelihood | 最大似然 |
maximum likelihood estimation | 最大似然估计 | 缩写 MLE
likelihood | 似然 |
method of moments | 矩估计法 |
sampling distribution | 抽样分布 |
standard error | 标准误 |
population | 总体 |
data-generating process | 数据生成过程 |

## 概率与分布
probability | 概率 |
uncertainty | 不确定性 |
random variable | 随机变量 |
distribution | 分布 |
probability distribution | 概率分布 |
probability density function | 概率密度函数 | 缩写 PDF
probability mass function | 概率质量函数 | 缩写 PMF
cumulative distribution function | 累积分布函数 | 缩写 CDF
expected value | 期望值 |
expectation | 期望 |
mean | 均值 |
standard deviation | 标准差 |
normal distribution | 正态分布 |
Gaussian | 高斯 |
binomial distribution | 二项分布 |
Poisson distribution | 泊松分布 |
uniform distribution | 均匀分布 |
exponential distribution | 指数分布 |
Bernoulli | 伯努利 |
joint distribution | 联合分布 |
marginal distribution | 边缘分布 |
conditional probability | 条件概率 |
independence | 独立性 |
independent and identically distributed | 独立同分布 | 缩写 i.i.d.
law of large numbers | 大数定律 |
central limit theorem | 中心极限定理 | 缩写 CLT

## 贝叶斯
Bayes' theorem | 贝叶斯定理 |
prior | 先验 |
posterior | 后验 |
likelihood | 似然 |
prior distribution | 先验分布 |
posterior distribution | 后验分布 |
conjugate prior | 共轭先验 |
credible interval | 可信区间 | 区别于置信区间 confidence interval
marginal likelihood | 边缘似然 |
evidence | 证据 | 贝叶斯语境亦指边缘似然
Markov chain Monte Carlo | 马尔可夫链蒙特卡洛 | 缩写 MCMC
Gibbs sampling | 吉布斯抽样 |
Metropolis-Hastings | Metropolis-Hastings 算法 | 保留人名
frequentist | 频率派 |
Bayesian | 贝叶斯派 | 作学派时；作定语作"贝叶斯"

## 假设检验
hypothesis testing | 假设检验 |
null hypothesis | 原假设 |
alternative hypothesis | 备择假设 |
significance level | 显著性水平 |
statistical significance | 统计显著性 |
Type I error | 第一类错误 |
Type II error | 第二类错误 |
power | 检验功效 | 统计功效
false positive | 假阳性 |
false negative | 假阴性 |
test statistic | 检验统计量 |
one-tailed | 单侧 |
two-tailed | 双侧 |
p-hacking | p 值操纵 |
multiple comparisons | 多重比较 |
Bonferroni correction | Bonferroni 校正 |
false discovery rate | 错误发现率 | 缩写 FDR
family-wise error rate | 族错误率 | 缩写 FWER
replication crisis | 可重复性危机 |
reproducibility | 可重复性 |

## 回归与模型
regression | 回归 |
linear regression | 线性回归 |
ordinary least squares | 普通最小二乘 | 缩写 OLS
coefficient | 系数 |
residual | 残差 |
generalized linear model | 广义线性模型 | 缩写 GLM
logistic regression | 逻辑回归 |
Poisson regression | 泊松回归 |
link function | 联系函数 |
interaction | 交互作用 |
model selection | 模型选择 |
bias-variance tradeoff | 偏差-方差权衡 |
underfitting | 欠拟合 |
cross-validation | 交叉验证 |
Akaike information criterion | 赤池信息准则 | 缩写 AIC
Bayesian information criterion | 贝叶斯信息准则 | 缩写 BIC
goodness of fit | 拟合优度 |

## 因果推断
causal inference | 因果推断 |
causation | 因果关系 |
correlation | 相关 | 与因果对立时强调"相关不等于因果"
confounder | 混杂因子 |
confounding | 混杂 |
Simpson's paradox | 辛普森悖论 |
directed acyclic graph | 有向无环图 | 缩写 DAG
counterfactual | 反事实 |
treatment | 处理 | 实验/因果语境
control group | 对照组 |
treatment group | 处理组 |
randomized controlled trial | 随机对照试验 | 缩写 RCT
instrumental variable | 工具变量 |
potential outcome | 潜在结果 |
average treatment effect | 平均处理效应 | 缩写 ATE
selection bias | 选择偏差 |

## AI / 评估
machine learning | 机器学习 |
neural network | 神经网络 |
overfitting | 过拟合 |
regularization | 正则化 |
hallucination | 幻觉 | LLM 语境
large language model | 大语言模型 | 缩写 LLM
precision | 精确率 | 分类评估
recall | 召回率 |
F1 score | F1 分数 |
confusion matrix | 混淆矩阵 |
ROC curve | ROC 曲线 |
AUC | AUC | 曲线下面积，保留
calibration | 校准 |
ground truth | 真实标签 |

## 抽样与设计
experimental design | 实验设计 |
survey methodology | 调查方法 |
sampling | 抽样 |
random sampling | 随机抽样 |
stratified sampling | 分层抽样 |
cluster sampling | 整群抽样 |
sample size | 样本量 |
response bias | 应答偏差 |
nonresponse bias | 无应答偏差 |
blocking | 区组 |
randomization | 随机化 |

## 时间序列与高维
time series | 时间序列 |
autocorrelation | 自相关 |
stationarity | 平稳性 |
trend | 趋势 |
seasonality | 季节性 |
high-dimensional | 高维 |
curse of dimensionality | 维数灾难 |
sparsity | 稀疏性 |
LASSO | LASSO | 保留
dimensionality reduction | 降维 |
principal component analysis | 主成分分析 | 缩写 PCA
