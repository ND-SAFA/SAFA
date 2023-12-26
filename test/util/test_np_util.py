import numpy as np

from tgen.common.util.np_util import NpUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestNpUtil(BaseTest):

    def test_convert_to_np_matrix(self):
        single_list = [1, 2, 3, 4, 5, 6]
        matrix = [[1, 2, 3], [4, 5, 6]]
        self.assertTrue(isinstance(NpUtil.convert_to_np_matrix(single_list), np.ndarray))
        converted_matrix = NpUtil.convert_to_np_matrix(matrix)
        self.assertTrue(isinstance(converted_matrix, np.ndarray))
        self.assertTrue(isinstance(converted_matrix[0, :], np.ndarray))
