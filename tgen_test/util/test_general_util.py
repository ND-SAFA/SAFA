from tgen.common.util.list_util import ListUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestListUtil(BaseTest):
    """
    Tests list utility methods.
    """

    def test_get_n_items_from_list(self):
        test_list = [i for i in range(50)]
        n_items_nums = [i for i in range(4, 10)]

        def verify(start):
            self.assertEqual(result[0], start)
            self.assertEqual(result[-1], (n_items - 1) + start)
            self.assertEqual(len(result), n_items)

        for i in range(0, 5, 2):
            for n_items in n_items_nums:
                expected_start = n_items * i
                result = ListUtil.get_n_items_from_list(test_list, n_items, iteration_num=i)[0]
                verify(expected_start)
                result = ListUtil.get_n_items_from_list(test_list, n_items, init_index=i)[0]
                verify(i)
