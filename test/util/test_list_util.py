from tgen.common.util.list_util import ListUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestListUtil(BaseTest):

    def test_safely_get_item(self):
        list_ = [1, 2, 3]
        self.assertEqual(ListUtil.safely_get_item(-3, list_), 1)
        self.assertEqual(ListUtil.safely_get_item(-4, list_), None)
        self.assertEqual(ListUtil.safely_get_item(0, list_), 1)
        self.assertEqual(ListUtil.safely_get_item(2, list_), 3)
        self.assertEqual(ListUtil.safely_get_item(3, list_), None)
