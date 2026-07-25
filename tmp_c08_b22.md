通用决策规则（值得记住）：当模型通过主要 provider API 且输出是 JSON 形态时用 **`instructor` + 原生 JSON schema**。当 (i) 模型自托管或 (ii) 约束比 JSON schema 更丰富（正则、文法）时用 **`outlines`**。代码库可以两者都用；按管道选择。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_对这四个场景中的每个，推荐 `instructor` + 原生 JSON schema vs. `outlines` 并简要论证。_ 你验证 (a) LLM 正确识别哪些场景是自托管 vs. provider API（决定因素；LLM 有时混淆这个），以及 (b) LLM 认识到 SQL 文法案例在 JSON schema 覆盖范围之外（常见 LLM 疏忽是声称 JSON schema 可表达任何约束；它不能）。

**Q6.** _跨章节：结构化输出作为第 6 章 prompt 注册表的基础_。将本章的判别联合模式与第 6 章的 prompt 注册表结合。注册表存储 prompt；结构化输出 schema 与每个 prompt 并存。设计集成：schema 存储在哪里、版本化如何交互、以及 prompt 和 schema 共版本的注册表的 eval 是什么样。

提示

§6.4 有注册表；§7.9 有 schema 和 prompt 协同设计模式。集成问题是如何一起版本化两者。

**答案：**

**存储布局。** 扩展 §6.4 的结构：每个 prompt 版本拥有其 schema。


    prompts/
    ├── manifest.yaml
    ├── clinical_summary/
    │   ├── v1/
    │   │   ├── prompt.md
    │   │   ├── schema.py
    │   │   └── eval_baseline.json
    │   ├── v2/
    │   │   ├── prompt.md
    │   │   ├── schema.py
    │   │   └── eval_baseline.json
    │   └── v3/
    │       ├── prompt.md
    │       ├── schema.py
    │       └── eval_baseline.json
    └── code_review/
        └── ...


每个版本目录包含 prompt 文本、Pydantic schema 和 eval 基线分数。Prompt 和 schema 一起版本化因为它们协同演化：schema 变更通常需要 prompt 变更（新变体需要新指令）反之亦然。独立版本化它们产生漂移，prompt 期望不存在的 schema 字段或反之。

**加载器。** 扩展 §6.4 加载器以从 `schema.py` 作为 Python 模块导入 schema：

    import importlib.util

    def load(self, name: str) -> tuple[Prompt, type[BaseModel]]:
        version = self.manifest[self.env][name]
        base = self.root / name / f"v{version}"
        prompt = self._load_prompt(base / "prompt.md")
        spec = importlib.util.spec_from_file_location(
            f"{name}_v{version}_schema",
            base / "schema.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        schema_cls = getattr(module, "Summary")  # 约定：联合命名为 `Summary`
        return prompt, schema_cls


加载器返回两个制品；调用者用 prompt 和 schema 一起调用模型。

**版本化交互。**
