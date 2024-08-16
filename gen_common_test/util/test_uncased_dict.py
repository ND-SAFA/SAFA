from gen_common.util import UncasedDict
from gen_common_test.base_tests.base_test import BaseTest


class TestUncasedDict(BaseTest):

    def test_process_key(self):
        uncased_dict = self.get_uncased_dict()
        self.assertEqual(uncased_dict._process_key("HELLO"), "hello")

    def test_process_value(self):
        uncased_dict = self.get_uncased_dict()
        value = {"PARENT": {"CHILD": {"GRANDCHILD": 2}}}
        processed_value = uncased_dict._process_value(value)
        self.assertIn("parent", processed_value)
        self.assertIn("child", processed_value["parent"])
        self.assertIn("grandchild", processed_value["parent"]["child"])
        self.assertEqual(2, processed_value["parent"]["child"]["grandchild"])

    def test_basic_functionality(self):
        uncased_dict = self.get_uncased_dict()
        self.assertIn("test", uncased_dict)
        self.assertEqual(uncased_dict["test"], 1)
        uncased_dict["test"] = 2
        self.assertEqual(uncased_dict["test"], 2)

    def get_uncased_dict(self):
        return UncasedDict({"TEST": 1})
