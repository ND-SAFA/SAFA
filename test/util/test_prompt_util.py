from tgen.common.util.prompt_util import PromptUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestPromptUtil(BaseTest):

    def test_create_xml(self):
        self.assertEqual(PromptUtil.create_xml("tag", "content"), "<tag>content</tag>")

    def test_format_as_markdown(self):
        self.assertEqual(PromptUtil.format_as_markdown("original"), "# original")
        self.assertEqual(PromptUtil.format_as_markdown("original", level=2), "## original")

    def test_strip_new_lines_and_extra_spaces(self):
        self.assertEqual(PromptUtil.strip_new_lines_and_extra_space("  \ntest\n "), "test")
