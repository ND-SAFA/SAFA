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
