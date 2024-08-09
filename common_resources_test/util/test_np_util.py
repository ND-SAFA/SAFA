import numpy as np

from common_resources.tools.util.np_util import NpUtil
from common_resources_test.base_tests.base_test import BaseTest


class TestNpUtil(BaseTest):

    def test_convert_to_np_matrix(self):
        single_list = [1, 2, 3, 4, 5, 6]
        matrix = [[1, 2, 3], [4, 5, 6]]
        self.assertTrue(isinstance(NpUtil.convert_to_np_matrix(single_list), np.ndarray))
        converted_matrix = NpUtil.convert_to_np_matrix(matrix)
        self.assertTrue(isinstance(converted_matrix, np.ndarray))
        self.assertTrue(isinstance(converted_matrix[0, :], np.ndarray))

    def test_detect_outlier_scores(self):
        list_ = [1, 2, 3, 4, 5]
        lower_threshold, upper_threshold = NpUtil.detect_outlier_scores(list_, ensure_at_least_one_detection=True)
        self.assertGreater(lower_threshold, list_[0])
        self.assertLess(upper_threshold, list_[-1])
