"""Static regression checks that can run without connecting to Discord or Google."""
import ast
import unittest
from unittest.mock import patch
import emojis
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "bot.py").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


def command_names():
    found = []
    for node in TREE.body:
        if isinstance(node, ast.AsyncFunctionDef):
            for decorator in node.decorator_list:
                text = ast.unparse(decorator)
                if "bot.tree.command" in text:
                    for keyword in getattr(decorator, "keywords", []):
                        if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
                            found.append(keyword.value.value)
    return set(found)


class SourceContractTests(unittest.TestCase):
    def test_existing_commands_preserved(self):
        expected = {"check", "type", "item", "add", "edit", "delete", "reload", "reportperms", "ping"}
        self.assertTrue(expected.issubset(command_names()))

    def test_owner_command_added(self):
        self.assertIn("botowner", command_names())

    def test_blocking_google_operations_are_offloaded_in_mutation_handlers(self):
        self.assertIn("await write_sheet_and_refresh(", SOURCE)
        self.assertIn("await refresh_data_async()", SOURCE)

    def test_bounded_normalization_cache_exists(self):
        self.assertIn("@lru_cache(maxsize=8192)", SOURCE)
        self.assertIn("_NORMALIZED_COLUMN_CACHE_MAX = 8", SOURCE)

    def test_components_v2_and_emoji_registry_are_used(self):
        self.assertIn("discord.ui.LayoutView", SOURCE)
        self.assertIn("ReportActionRow", SOURCE)
        self.assertTrue((ROOT / "emojis.py").exists())
        self.assertIn("from emojis import emoji as get_emoji", SOURCE)

    def test_emoji_registry_has_unicode_fallback_and_custom_markup(self):
        self.assertEqual(emojis.emoji("success"), "✅")
        with patch.dict("os.environ", {
            "EMOJI_SUCCESS_NAME": "custom_check",
            "EMOJI_SUCCESS_ID": "123456789012345678",
            "EMOJI_SUCCESS_ANIMATED": "false",
        }, clear=False):
            self.assertEqual(emojis.emoji("success"), "<:custom_check:123456789012345678>")
        with patch.dict("os.environ", {
            "EMOJI_SUCCESS_NAME": "custom_check",
            "EMOJI_SUCCESS_ID": "123456789012345678",
            "EMOJI_SUCCESS_ANIMATED": "true",
        }, clear=False):
            self.assertEqual(emojis.emoji("success"), "<a:custom_check:123456789012345678>")

    def test_no_hardcoded_secrets(self):
        self.assertNotIn("MTA", SOURCE)
        self.assertIn('TOKEN = os.getenv("TOKEN")', SOURCE)


if __name__ == "__main__":
    unittest.main()
