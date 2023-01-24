from unittest import TestCase

from scripts.script_utils import get_dict_path


class TestScriptUtils(TestCase):
    def test_multiple_values(self):
        data = {"first": 42, "second": 36}
        data_path = [["first", "second"]]
        query_result = get_dict_path(data, data_path)
        self.assertEqual(1, len(query_result))
        query = query_result[0]
        self.assertDictEqual(data, query)

    def test_lists(self):
        data = {"items": [{"a": 42, "b": 36}, {"a": 36, "b": 42}]}
        data_path = ["items", ["a", "b"]]
        query_result = get_dict_path(data, data_path)
        self.assertEqual(2, len(query_result))
        self.assertDictEqual({"a": 42, "b": 36}, query_result[0])
        self.assertDictEqual({"a": 36, "b": 42}, query_result[1])

    def test_get_dict_path(self):
        data = {
            "parent": {
                "child": [{"first": 42, "second": 36}, {"first": 36, "second": 42}]
            }
        }
        data_path = ["parent", "child", ["first", "second"]]
        expected = data["parent"]["child"]
        query_result = get_dict_path(data, data_path)
        self.assertEqual(2, len(query_result))
        self.assertListEqual(expected, query_result)
