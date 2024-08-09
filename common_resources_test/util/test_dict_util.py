import math
import string
from unittest import TestCase

from common_resources.tools.util.dict_util import DictUtil


class TestDictUtil(TestCase):
    """
    Responsible for testing that dictionary utility is correct.
    """

    def test_initialize_value_if_not_in_dict(self):
        dict_ = {1: [2, 3]}
        self.assertFalse(DictUtil.initialize_value_if_not_in_dict(dict_, 1, []))
        self.assertListEqual(dict_[1], [2, 3])
        self.assertTrue(DictUtil.initialize_value_if_not_in_dict(dict_, 2, []))
        self.assertIn(2, dict_)
        self.assertIsInstance(dict_[2], list)

    def test_assert_same_keys(self):
        """
        Tests that same keys.
        """
        link_a = {"a": 1, "b": 2}
        link_b = {"b": 2, "a": 1}
        DictUtil.assert_same_keys([link_a, link_b])

    def test_assert_same_keys_error(self):
        """
        Tests that different keys throw error
        """
        link_a = {"a": 1, "b": 2}
        link_b = {"b": 1, "c": 1}
        with self.assertRaises(Exception) as e:
            DictUtil.assert_same_keys([link_a, link_b])

    def test_combine_child_dicts(self):
        parent = {"A": {"1": "hello", "2": "what's"},
                  "B": {"3": "world", "4": "up"},
                  "C": {"5": "don't combine"}}
        keys2combine = {"A", "B"}
        combined = DictUtil.combine_child_dicts(parent, keys2combine)
        for key, val in parent.items():
            if key in keys2combine:
                for k, v in val.items():
                    self.assertIn(k, combined)
            else:
                for k, v in val.items():
                    self.assertNotIn(k, combined)

    def test_filter_dict_keys(self):
        dict_ = {"A": {"1": "hello", "2": "what's"},
                 "B": {"3": "world", "4": "up"},
                 "C": {"5": "filter me"}}
        keys2keep = {"A", "B"}
        filtered1 = DictUtil.filter_dict_keys(dict_, keys2keep=keys2keep)
        filtered2 = DictUtil.filter_dict_keys(dict_, keys2filter={"C"})
        for filtered in [filtered1, filtered2]:
            for k, v in filtered.items():
                if k in keys2keep:
                    self.assertIn(k, filtered)
                else:
                    self.assertNotIn(k, filtered)

    def test_joining(self):
        dict_ = [{"1": "hello ", "2": "what's "}, {"1": "world", "2": "up"}]
        joined = DictUtil.joining(dict_)
        self.assertIn("1", joined)
        self.assertEqual(joined["1"], "hello world")
        self.assertIn("2", joined)
        self.assertEqual(joined["2"], "what's up")

    def test_get_kwarg_values(self):
        kwargs = {"one": 1, "two": 2, "three": 3}
        values = DictUtil.get_dict_values(kwargs, pop=False, one=None, four=4)
        self.assertEqual(values[0], 1)
        self.assertEqual(values[1], 4)

        value = DictUtil.get_dict_values(kwargs, pop=True, one=None)
        self.assertEqual(value, 1)
        self.assertNotIn("one", kwargs)

    def test_update_kwarg_values(self):
        kwargs = {"one": 1, "two": 2, "three": 3}
        DictUtil.update_kwarg_values(kwargs, replace_existing=True, one="uno", four=4)
        self.assertEqual(kwargs["one"], "uno")
        self.assertIn("four", kwargs)
        DictUtil.update_kwarg_values(kwargs, replace_existing=False, four="cuatro", five=5)
        self.assertNotEqual(kwargs["four"], "cuatro")
        self.assertIn("five", kwargs)

    def test_flip(self):

        # basic case
        orig = {k: i for i, k in enumerate(string.ascii_lowercase[:3])}
        expected = {i: k for i, k in enumerate(string.ascii_lowercase[:3])}
        flipped = DictUtil.flip(orig)
        self.assertDictEqual(flipped, expected)

        # values are lists
        orig = {i: list(string.ascii_lowercase[i * 3:i * 3 + 3]) for i in range(3)}
        expected = {k: math.floor(i / 3) for i, k in enumerate(string.ascii_lowercase[:9])}
        flipped = DictUtil.flip(orig)
        self.assertDictEqual(flipped, expected)

        # value maps to multiple keys
        orig = {i: list(string.ascii_lowercase[i * 3:i * 3 + 4]) for i in range(3)}
        expected_values = [min(math.floor(i / 3), 2) for i in range(10)]
        expected = {k: ([v - 1, v] if i % 3 == 0 and 0 < i < 9 else [v])
                    for i, (k, v) in enumerate(zip(string.ascii_lowercase[:10], expected_values))}
        flipped = DictUtil.flip(orig)
        self.assertDictEqual(flipped, expected)

    def test_set_or_increment_item(self):
        dict_ = {"a": 1}
        DictUtil.set_or_increment_count(dict_, "a", 3)
        self.assertEqual(dict_["a"], 4)
        DictUtil.set_or_increment_count(dict_, "b", 3)
        self.assertEqual(dict_["b"], 3)

    def test_set_or_append_item(self):
        dict_ = {"a": [1, 2]}
        DictUtil.set_or_append_item(dict_, "a", 3)
        DictUtil.set_or_append_item(dict_, "b", 4)
        DictUtil.set_or_append_item(dict_, "b", [5, 6])
        self.assertListEqual(dict_["a"], [1, 2, 3])
        self.assertIn("b", dict_)
        self.assertListEqual(dict_["b"], [4, 5, 6])
