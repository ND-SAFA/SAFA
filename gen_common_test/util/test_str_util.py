import uuid

from gen_common.util.str_util import StrUtil
from gen_common_test.base.tests.base_test import BaseTest


class TestStrUtil(BaseTest):

    def test_split_by_punctuation(self):
        input_string = "no punctuation"
        self.assertEqual(StrUtil.split_by_punctuation(input_string)[0], input_string)
        input_string = "there? is punctuation; in string!"
        split_string = StrUtil.split_by_punctuation(input_string)
        self.assertEqual(split_string[0], "there")
        self.assertEqual(split_string[1], "is punctuation")
        self.assertEqual(split_string[2], "in string")

    def test_format_selective(self):
        str2format = "I need to format these: {one} {two} but not this: {three}"
        formatted = StrUtil.format_selective(str2format, "random", one="A", two="B")
        self.assertEqual(formatted, "I need to format these: A B but not this: {three}")

        str2format = "I need to format these: {} {} but not this: {}"
        formatted = StrUtil.format_selective(str2format, "A", "B", random="four")
        self.assertEqual(formatted, "I need to format these: A B but not this: {}")

        str2format = "I need to format these: {} and {this} but not this {}"
        formatted = StrUtil.format_selective(str2format, "A", this="B", random="four")
        self.assertEqual(formatted, "I need to format these: A and B but not this {}")

        str2format = "Nothing should be formatted: {} and {this}"
        formatted = StrUtil.format_selective(str2format, random="four")
        self.assertEqual(formatted, "Nothing should be formatted: {} and {this}")

    def test_get_letter_from_number(self):
        self.assertEqual(StrUtil.get_letter_from_number(10, lower_case=True), "k")
        self.assertEqual(StrUtil.get_letter_from_number(10, lower_case=False), "K")

    def test_is_uuid(self):
        self.assertTrue(StrUtil.is_uuid(str(uuid.uuid4())))
        self.assertFalse(StrUtil.is_uuid("hello world"))

    def test_snake_case_to_pascal_case(self):
        self.assertEqual("SnakeCase", StrUtil.snake_case_to_pascal_case("snake_case"))

    def test_split_sentences_by_period(self):
        sentences = ["This is a sentence with 2.3 in it and K.R.D but it should on be split", "Here", "And Here"]
        self.assertEqual(StrUtil.split_sentences_by_punctuation(". ".join(sentences)), sentences)

        self.assertEqual(StrUtil.split_sentences_by_punctuation(", ".join(sentences), ","), sentences)

    def test_remove_floats_and_ints(self):
        sentence = "This is a sentence with 2.3 in it which should be removed but RE.2.3 and 2 should not 3.0"
        self.assertEqual(StrUtil.remove_floats(sentence),
                         "This is a sentence with  in it which should be removed but RE.2.3 and 2 should not")

    def test_remove_chars(self):
        string = "<These ^ chars ? need to be removed />"
        removed_chars_string = StrUtil.remove_substrings(string, ["?", "^", "/>", "<"])
        self.assertEqual("These  chars  need to be removed ", removed_chars_string)

        removed_chars_string = StrUtil.remove_substrings(string, "<")
        self.assertEqual("These ^ chars ? need to be removed />", removed_chars_string)

    def test_remove_decimal_points_from_floats(self):
        string = "blah1.23something. and 4.56another 7.890here."
        result = StrUtil.remove_decimal_points_from_floats(string)
        self.assertEqual("blah1something. and 4another 7here.", result)

    def test_remove_substring(self):
        string = "hitesthitesthi"
        substring = "hi"
        remove_all = StrUtil.remove_substring(string, substring)
        self.assertNotIn(substring, remove_all)

        remove_first = StrUtil.remove_substring(string, substring, only_if_startswith=True)
        self.assertFalse(remove_first.startswith(substring))
        self.assertIn(substring, remove_first)

        remove_last = StrUtil.remove_substring(string, substring, only_if_endswith=True)
        self.assertFalse(remove_last.endswith(substring))
        self.assertIn(substring, remove_last)

    def test_convert_all_items_to_string(self):
        self.assertEqual(StrUtil.convert_all_items_to_string([1, 2, 3]), ['1', '2', '3'])
        self.assertEqual(StrUtil.convert_all_items_to_string({1, 2, 3}), {'1', '2', '3'})
        self.assertEqual(StrUtil.convert_all_items_to_string({1: False, 2: True, 3: False}), {'1': 'False', '2': 'True', '3': 'False'})

    def test_separate_joined_word(self):
        self.assertEqual(StrUtil.separate_joined_words("HelloWorld"), "Hello World")
        self.assertEqual(StrUtil.separate_joined_words("hello_world"), "hello world")

    def test_fill_with_format_variable_name(self):
        self.assertEqual(StrUtil.fill_with_format_variable_name("The {} in the {}", "cat", count=1), "The {cat} in the {}")
        self.assertEqual(StrUtil.fill_with_format_variable_name("The {} in the {}", "hat", count=-1), "The {hat} in the {hat}")

    def test_remove_stop_words(self):
        self.assertEqual(StrUtil.remove_stop_words("The cat in the hat"), "cat hat")

    def test_find_start_and_end_loc(self):
        main_string = "The cat in the hat"
        str2find = "cat"
        bad_case = str2find.upper()
        expected_index = main_string.find(str2find)
        start_and_end = (expected_index, expected_index + 3)
        not_found = (-1, -1)
        self.assertEqual(StrUtil.find_start_and_end_loc(main_string, str2find), start_and_end)
        self.assertEqual(StrUtil.find_start_and_end_loc(main_string, bad_case), not_found)
        self.assertEqual(StrUtil.find_start_and_end_loc(main_string, bad_case, ignore_case=True), start_and_end)

        str2find = "at"
        start_and_end = (start_and_end[0] + 1, start_and_end[-1])
        self.assertEqual(StrUtil.find_start_and_end_loc(main_string, str2find), start_and_end)
        self.assertEqual(StrUtil.find_start_and_end_loc(main_string, str2find, start=start_and_end[-1])[0], len(main_string) - 2)
        self.assertEqual(StrUtil.find_start_and_end_loc(main_string, str2find, end=1), not_found)
