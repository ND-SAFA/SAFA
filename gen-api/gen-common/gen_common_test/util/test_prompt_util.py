from gen_common.util.prompt_util import PromptUtil
from gen_common_test.base.tests.base_test import BaseTest


class TestPromptUtil(BaseTest):

    def test_create_xml(self):
        self.assertEqual(PromptUtil.create_xml("tag", "content"), "<tag>content</tag>")

    def test_format_as_markdown(self):
        self.assertEqual(PromptUtil.as_markdown_header("original"), "# original")
        self.assertEqual(PromptUtil.as_markdown_header("original", level=2), "## original")

    def test_strip_new_lines_and_extra_spaces(self):
        self.assertEqual(PromptUtil.strip_new_lines_and_extra_space("  \ntest\n "), "test")

    def test_format_as_bullet_point(self):
        bullets = ['*', '-', '+']
        high_level = PromptUtil.as_bullet_point("high-level", level=1)
        self.assertIn(bullets[0], high_level)
        self.assertEqual(0, high_level.count("\t"))
        mid_level = PromptUtil.as_bullet_point("med-level", level=2)
        self.assertIn(bullets[1], mid_level)
        self.assertEqual(1, mid_level.count("\t"))
        low_level = PromptUtil.as_bullet_point("low-level", level=3)
        self.assertIn(bullets[2], low_level)
        self.assertEqual(2, low_level.count("\t"))
        lowest_level = PromptUtil.as_bullet_point("lowest-level", level=4)
        self.assertIn(bullets[0], lowest_level)
        self.assertEqual(3, lowest_level.count("\t"))

    def test_indent_for_markdown(self):
        self.assertEqual(PromptUtil.indent_for_markdown("test", 2), "        test")
