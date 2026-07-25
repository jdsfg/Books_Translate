**答案：**


    import re
    import logging
    from dataclasses import dataclass
    from enum import Enum
    from typing import Optional

    logger = logging.getLogger("security.injection")

    class ScreeningMode(Enum):
        FLAGGING = "flagging"  # 检测并记录；不阻止
        STRICT = "strict"      # 阻止检测到的内容

    @dataclass
    class InjectionScreeningResult:
        detected: bool
        pattern_matched: Optional[str]
        sample_context: Optional[str]  # 匹配周围 100 字符用于日志

    # 选择为生产流量中常见的模式
    INJECTION_PATTERNS = [
        (
            "ignore_instructions",
            re.compile(r"(?i)\b(ignore|disregard|forget)\s+(all\s+)?(previous|prior|above|system|the)\s+(instruction|prompt|message|rule|order)s?\b"),
        ),
        (
            "role_redefinition",
            re.compile(r"(?i)\byou\s+are\s+(now\s+)?a\s+(different|new)\s+(assistant|ai|bot|agent|persona)\b"),
        ),
        (
            "system_prompt_reveal",
            re.compile(r"(?i)\b(reveal|show|tell|display|print)\s+(me\s+)?(your\s+|the\s+)?(system\s+)?(prompt|instructions|configuration)\b"),
        ),
        (
            "fake_system_tag",
            re.compile(r"<\s*(system|admin|sudo|root)\s*>", re.IGNORECASE),
        ),
        # 2026 现实模式：2026 威胁模型不再是 DAN 风格
        # 越狱短语（现代前沿模型被训练拒绝那些）；
        # 真正风险是工具调用欺骗、角色混淆标签注入、
        # 和通过检索内容的零宽/隐藏 Unicode 走私。
        (
            "tool_call_spoof",
            re.compile(r"(?i)<\s*tool[_\s]?(call|use|response)\s*>"),
        ),
        (
            "role_confusion_tag",
            re.compile(r"<\s*\|im_(start|end)\s*\|\s*>"),
        ),
        (
            "hidden_unicode_smuggling",
            # 对抗者用于走私 prompt 内容绕过人工审查和简单筛查的
            # 零宽和双向覆盖 Unicode 范围。
            # 范围：
            #   U+200B–U+200F : ZWSP, ZWNJ, ZWJ, LRM, RLM
            #   U+202A–U+202E : LRE, RLE, PDF, LRO, RLO（双向覆盖）
            #   U+2060–U+206F : 词连接符，功能控制
            #   U+FEFF        : BOM / 零宽无断空格
            re.compile(
                "["
                "\u200B-\u200F"   # ZWSP, ZWNJ, ZWJ, LRM, RLM
                "\u202A-\u202E"   # LRE, RLE, PDF, LRO, RLO（双向覆盖）
                "\u2060-\u206F"   # 词连接符，功能控制
                "\uFEFF"           # BOM / 零宽无断空格
                "]"
            ),
        ),
        # 遗留短语模式：2026 年低优先级但仍偶尔出现。
        # 现代前沿模型自行可靠拒绝这些；我们保留
        # 筛查仅用于遥测（了解攻击面正在被探测）。
        (
            "legacy_jailbreak_phrase",
            re.compile(r"(?i)\b(DAN\s+mode|do\s+anything\s+now|developer\s+mode\s+enabled)\b"),
        ),
    ]

    def screen_for_injection(
        content: str,
        source_id: str,
        request_id: str,
        mode: ScreeningMode = ScreeningMode.FLAGGING,
    ) -> InjectionScreeningResult:
        for pattern_name, pattern in INJECTION_PATTERNS:
            match = pattern.search(content)
            if match:
                # 捕获匹配周围的上下文用于日志
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end]

                result = InjectionScreeningResult(
                    detected=True,
                    pattern_matched=pattern_name,
                    sample_context=context,
                )

                logger.warning(
                    "injection_pattern_detected",
                    extra={
                        "request_id": request_id,
                        "source_id": source_id,
                        "pattern_name": pattern_name,
                        "context_snippet": context,
                        "mode": mode.value,
                    },
                )

                return result

        return InjectionScreeningResult(detected=False, pattern_matched=None, sample_context=None)


    def process_with_screening(
        content: str,
        source_id: str,
        request_id: str,
        mode: ScreeningMode,
    ) -> str:
        result = screen_for_injection(content, source_id, request_id, mode)
        if result.detected and mode == ScreeningMode.STRICT:
            raise PermissionError(f"injection pattern '{result.pattern_matched}' detected; strict mode blocks content")
        return content  # 标记模式下，内容带日志通过
