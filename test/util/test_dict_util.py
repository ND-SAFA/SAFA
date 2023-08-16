from unittest import TestCase

from tgen.common.util.dict_util import DictUtil


class TestDictUtil(TestCase):
    """
    Responsible for testing that dictionary utility is correct.
    """

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
        keys2combine =  {"A", "B"}
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
            for k,v in filtered.items():
                if k in keys2keep:
                    self.assertIn(k, filtered)
                else:
                    self.assertNotIn(k, filtered)

    def test_joining(self):
        dict_ = [{"1": "hello ", "2": "what's "},  {"1": "world", "2": "up"}]
        joined = DictUtil.joining(dict_)
        self.assertIn("1", joined)
        self.assertEqual(joined["1"], "hello world")
        self.assertIn("2", joined)
        self.assertEqual(joined["2"], "what's up")
