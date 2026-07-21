import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


TRANSLATE_DIR = Path(__file__).resolve().parents[1]


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, TRANSLATE_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit = load_module("audit_translation_test", "audit_translation.py")
publisher = load_module("publish_audit_comment_test", "publish_audit_comment.py")


class AuditHelpersTest(unittest.TestCase):
    def test_question_ids_support_english_and_chinese_labels(self):
        text = "\n".join(
            [
                "**Q1.** First",
                "**问2.** 第二",
                "**问题3。** 第三",
                "**答：** ignored",
            ]
        )
        self.assertEqual(audit.question_ids(text), {"1": 1, "2": 1, "3": 1})

    def test_normalized_paragraphs_ignore_short_content(self):
        repeated = "这是一段用于检测相邻块重复的长文本。" * 15
        paragraphs = audit.normalized_paragraphs(f"短句\n\n**{repeated}**")
        self.assertEqual(paragraphs, {repeated})

    def test_changed_books_selects_only_matching_book(self):
        config = {
            "books": {
                "甲": {"source": "sources/甲.md"},
                "乙": {"source": "sources/乙.md"},
            }
        }
        paths = ["pipeline/translate/乙/blocks/c01_b01.md", "README.md"]
        self.assertEqual(audit.changed_books(config, paths), ["乙"])

    def test_generated_translation_is_blocking(self):
        findings = audit.audit_changed_paths(["sources/甲.zh.md", "notes.log", "README.md"])
        self.assertEqual([finding.code for finding in findings], ["PROHIBITED_FILE"] * 2)

    def test_new_book_requires_review_registration(self):
        config = {"books": {"甲": {"source": "sources/甲.md"}}}
        findings = audit.audit_book_registration(
            config,
            ["sources/乙.md", "pipeline/translate/乙/checkpoint.json"],
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].code, "BOOK_NOT_REGISTERED")

    def test_source_placeholders_are_not_false_positives(self):
        self.assertFalse(audit.unexpected_placeholders("变量 XXX", "变量 XXX"))
        self.assertEqual(audit.unexpected_placeholders("变量", "变量 XXX"), {"XXX": 1})

    def test_translation_only_duplicate_is_detected(self):
        paragraph = "用于检测重复的完整长段落。" * 20
        self.assertFalse(
            audit.duplicated_paragraphs_beyond_source(
                f"{paragraph}\n\n{paragraph}",
                f"{paragraph}\n\n{paragraph}",
            )
        )
        self.assertEqual(
            audit.duplicated_paragraphs_beyond_source(
                paragraph,
                f"{paragraph}\n\n{paragraph}",
            ),
            [paragraph],
        )

    def test_report_distinguishes_mechanical_pass(self):
        result = audit.BookResult(book="甲", done=1, total=2, assembled=True)
        report = audit.render_report([result], [], ["pipeline/translate/甲/checkpoint.json"])
        self.assertIn("MECHANICAL PASS", report)
        self.assertIn("independent source/translation semantic review", report)


class PublishCommentTest(unittest.TestCase):
    @patch.object(publisher, "request_json")
    def test_publish_updates_existing_marker_comment(self, request_json):
        request_json.side_effect = [
            [{"body": f"{publisher.MARKER}\nold", "url": "https://api.example/comment/1"}],
            {},
        ]
        action = publisher.publish("owner/repo", 3, f"{publisher.MARKER}\nnew", "token")
        self.assertEqual(action, "updated")
        self.assertEqual(request_json.call_args_list[1].args[2], "PATCH")

    @patch.object(publisher, "request_json")
    def test_publish_creates_comment_when_marker_is_absent(self, request_json):
        request_json.side_effect = [[], {}]
        action = publisher.publish("owner/repo", 3, f"{publisher.MARKER}\nnew", "token")
        self.assertEqual(action, "created")
        self.assertEqual(request_json.call_args_list[1].args[2], "POST")


if __name__ == "__main__":
    unittest.main()
