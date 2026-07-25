**答案：** 有用的 prompt：_为代码搜索功能设计追踪 schema：轨迹字段、LLM 调用字段、工具调用字段、eval 分数集成。_ 你验证 (a) schema 捕获轨迹级结构（LLM 可能默认仅每调用；坚持轨迹包装器），以及 (b) 你实际会在仪表板中查询的字段被包含（LLM 可能产生有你不用字段的 schema；对照你的运维需求检查）。

**Q2.** _构建 PHI 脱敏层_。实现 §19.7 的 `redact_phi` 函数，带：(a) 5 种 PHI 类型的模式；(b) 演示正确脱敏的单元测试；(c) 假阳性与假阴性之间权衡的处理。

**答案：**


    import re
    from dataclasses import dataclass

    @dataclass
    class RedactionPattern:
        name: str
        pattern: re.Pattern
        replacement: str
        description: str

    PHI_PATTERNS = [
        RedactionPattern(
            "name",
            re.compile(r"\b(Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)*\b"),
            "[NAME]",
            "带称谓的姓名：Mr/Mrs/Ms/Dr 后跟大写单词",
        ),
        RedactionPattern(
            "dob",
            re.compile(r"\bdob:?\s*(0[1-9]|1[0-2])[/-](0[1-9]|[12]\d|3[01])[/-](19|20)\d{2}\b", re.IGNORECASE),
            "[DOB]",
            "DOB 后跟 mm/dd/yyyy 格式日期",
        ),
        RedactionPattern(
            "date_only",
            re.compile(r"\b(0[1-9]|1[0-2])[/-](0[1-9]|[12]\d|3[01])[/-](19|20)\d{2}\b"),
            "[DATE]",
            "独立日期",
        ),
        RedactionPattern(
            "mrn",
            re.compile(r"\bMRN[-:]?\s*\d{6,10}\b", re.IGNORECASE),
            "[MRN]",
            "病历号",
        ),
        RedactionPattern(
            "ssn",
            re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "[SSN]",
            "社会安全号",
        ),
    ]

    def redact_phi(text: str, aggressive: bool = False) -> str:
        """应用 PHI 脱敏。aggressive=True 时包含更广模式
        （date_only），有对非 PHI 日期假阳性的风险。"""
        redacted = text
        for p in PHI_PATTERNS:
            if p.name == "date_only" and not aggressive:
                continue
            redacted = p.pattern.sub(p.replacement, redacted)
        return redacted

    # 单元测试
    def test_redact_phi():
        assert redact_phi("Patient Mr. John Smith presented with...") == "Patient [NAME] presented with..."
        # DOB 正则一起消费 "DOB:" 前缀 + 日期，所以
        # 整个匹配被替换字符串替换。如想保留 "DOB:" 前缀，
        # 用 lookbehind: r"(?i)(?<=dob:)\s*..."
        assert redact_phi("DOB: 03/15/1965") == "[DOB]"
        assert redact_phi("MRN-12345678 visited the clinic") == "[MRN] visited the clinic"
        assert redact_phi("SSN 123-45-6789 was provided") == "SSN [SSN] was provided"
        # aggressive=True 时，非 DOB 日期通过
        assert "01/15/2024" in redact_phi("Last visit was 01/15/2024")
        # aggressive=True 时，它们被脱敏（假阳性风险）
        assert "[DATE]" in redact_phi("Last visit was 01/15/2024", aggressive=True)

    test_redact_phi()


**假阳性 vs 假阴性权衡处理**：
