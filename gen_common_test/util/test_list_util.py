from gen_common.util import ListUtil
from gen_common_test.base_tests.base_test import BaseTest


class TestListUtil(BaseTest):

    def test_safely_get_item(self):
        list_ = [1, 2, 3]
        self.assertEqual(ListUtil.safely_get_item(-3, list_), 1)
        self.assertEqual(ListUtil.safely_get_item(-4, list_), None)
        self.assertEqual(ListUtil.safely_get_item(0, list_), 1)
        self.assertEqual(ListUtil.safely_get_item(2, list_), 3)
        self.assertEqual(ListUtil.safely_get_item(3, list_), None)

    def test_are_all_items_the_same(self):
        self.assertTrue(ListUtil.are_all_items_the_same([1, 1, 1]))
        self.assertFalse(ListUtil.are_all_items_the_same([1, 2, 1]))

    def test_get_max_value_with_index(self):
        list_ = [1, 3, 2, 3, 1]
        index, max_val = ListUtil.get_max_value_with_index(list_)
        self.assertEqual(max_val, max(list_))
        self.assertEqual(index, list_.index(max(list_)))
