import uuid

from tgen.common.util.str_util import StrUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestStrUtil(BaseTest):

    def test_format_selective(self):
        str2format = "I need to format these: {one} {two} but not this: {three}"
        formatted = StrUtil.format_selective(str2format, "random", one="A", two="B")
        self.assertEqual(formatted, "I need to format these: A B but not this: {three}")

        str2format = "I need to format these: {} {} but not this: {}"
        formatted = StrUtil.format_selective(str2format, "A", "B", random="four")
        self.assertEqual(formatted, "I need to format these: A B but not this: {}")

        str2format = "I need to format these: {} and {this} but not this {}"
        formatted = StrUtil.format_selective(str2format, "A", this="B",  random="four")
        self.assertEqual(formatted, "I need to format these: A and B but not this {}")

        str2format = "Nothing should be formatted: {} and {this}"
        formatted = StrUtil.format_selective(str2format,  random="four")
        self.assertEqual(formatted, "Nothing should be formatted: {} and {this}")

    def test_is_uuid(self):
        self.assertTrue(StrUtil.is_uuid(str(uuid.uuid4())))
        self.assertFalse(StrUtil.is_uuid("hello world"))

    def test_snake_case_to_pascal_case(self):
        self.assertEqual("SnakeCase", StrUtil.snake_case_to_pascal_case("snake_case"))
