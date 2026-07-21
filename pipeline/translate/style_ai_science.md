# 风格简报 · AI Science 系列（ai_sci_I / ai_sci_II / ai_eng）

> 覆盖：AI 科学 I：从神经网络到 Transformer / AI 科学 II：大语言模型 / AI 工程：用 LLM 构建生产系统。技术/科学书，**质量 bar = 准确 + 通顺 + 领域惯例**，内容精度 > 文采。

## 1. 系列定位
AI/ML 科普到半技术。讲神经网络、注意力、Transformer、LLM、以及生产级 LLM 应用工程。受众有技术背景。

## 2. 质量 bar（核心）
- **准确优先**：术语、公式、数值、架构描述零容错。
- **领域惯例**：被动语态可保留；代码注释照译；公式/符号原样。
- **通顺**：长难句可拆，但不可丢逻辑连接。

## 3. 人称 / 语气
- 中性陈述为主；保留作者适度的"我们"示例口吻（如有）。
- 不添加原书没有的观点或最新进展（避免时效错位）。

## 4. 术语处理（关键）
- 首现加注原文：transformer（Transformer）、attention（注意力）、embedding（嵌入）、tokenizer（分词器）、fine-tuning（微调）、pretraining（预训练）、RAG（检索增强生成）、agent（智能体）、inference（推理）、latent space（潜空间）、backpropagation（反向传播）、gradient（梯度）、loss（损失）、hallucination（幻觉）、context window（上下文窗口）。
- 模型/架构名保留英文（GPT、BERT、Transformer），不硬译。

## 5. 禁忌译法
- training = 训练（ML 语境），非"练习"。
- inference = 推理（ML 语境），非"推断/结论"。
- token = 词元/令牌，按惯例用"词元"；上下文用"token"可保留。
- 不把参数规模（7B、175B）改成中文数词。

## 6. 结构保全
- 代码块、LaTeX 公式（$/$$）、表格、脚注、标题层级原样。
- 架构图注、伪代码保留。

## 7. 数字规则（强制阿拉伯 + 原单位）
- 模型规模（7B / 175B 参数）、维度（768-dim）、百分比（92.3%）、温度（0.7）、层数（12 层）、序列长度（2048）一律阿拉伯数字 + 原单位。
- 公式内符号（N、d_model、η）原样，不译。

## 8. 示例
- 源：`The attention mechanism computes a weighted sum of values.`
- 译：`注意力机制计算 values 的加权和。`
- 源：`GPT-3 has 175B parameters and a context window of 2048 tokens.`
- 译：`GPT-3 拥有 175B 参数，上下文窗口为 2048 个 token。`

---

_最后更新：2026-07-19。技术系列记"精度与惯例"；数字强制阿拉伯+原单位。_
