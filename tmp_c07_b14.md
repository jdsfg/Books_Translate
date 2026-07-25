#### 应用题

**Q1.** _为你的团队设计 prompt 注册表_。勾勒支持以下功能的 prompt 注册表的文件布局、清单 schema 和加载器代码：(a) 多个 prompt 名称；(b) 每 prompt 版本化；(c) 每环境清单；(d) 返回 prompt 文本加关联模型和参数的加载器。

提示

§6.4 有结构；充实它。

**答案：**

文件布局：


    prompts/
    ├── manifest.yaml
    ├── clinical_summary/
    │   ├── v1.md
    │   ├── v2.md
    │   └── v3.md
    └── code_review/
        ├── v1.md
        └── v2.md


清单：


    production:
      clinical_summary: v3
      code_review: v2
    staging:
      clinical_summary: v4-candidate
      code_review: v2
    dev:
      clinical_summary: v4-candidate
      code_review: v2-experimental


每个 prompt 文件（`v3.md`）：


    ---
    prompt_name: clinical_summary
    version: 3
    model: claude-sonnet-4-20260315
    temperature: 0
    max_tokens: 1024
    created_at: 2026-02-14
    eval_baseline_score: 9.4
    ---

    你是 Beacon Health AI 的临床笔记摘要器。
    ...


加载器代码：


    from pathlib import Path
    from dataclasses import dataclass
    import os
    import yaml

    @dataclass
    class Prompt:
        name: str
        version: str
        text: str
        model: str
        temperature: float
        max_tokens: int

    class PromptRegistry:
        def __init__(self, root: Path, env: str | None = None):
            self.root = root
            self.env = env or os.environ.get("APP_ENV", "production")
            with (root / "manifest.yaml").open() as f:
                self.manifest = yaml.safe_load(f)

        def load(self, name: str) -> Prompt:
            version = self.manifest[self.env][name]
            path = self.root / name / f"{version}.md"
            text = path.read_text()
            frontmatter, body = self._split(text)
            return Prompt(
                name=name,
                version=version,
                text=body.strip(),
                model=frontmatter["model"],
                temperature=frontmatter.get("temperature", 0),
                max_tokens=frontmatter.get("max_tokens", 1024),
            )

        @staticmethod
        def _split(text: str) -> tuple[dict, str]:
            if not text.startswith("---"):
                raise ValueError("prompt file missing front-matter")
            _, fm, body = text.split("---", 2)
            return yaml.safe_load(fm), body


用法：


    registry = PromptRegistry(Path("prompts"))
    prompt = registry.load("clinical_summary")
    response = client.messages.create(
        model=prompt.model,
        max_tokens=prompt.max_tokens,
        system=prompt.text,
        messages=[{"role": "user", "content": note}],
        temperature=prompt.temperature,
    )


这大约是最小可行注册表。扩展：惰性加载 + 缓存、prompt 哈希验证（捕获意外编辑）、跨环境 diff CLI、附加到每个版本的 eval 分数历史。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？
