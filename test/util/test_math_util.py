from tgen.common.util.math_util import MathUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestMathUtil(BaseTest):

    def test_safely_get_item(self):
        self.assertEqual(MathUtil.round_to_nearest_half(1.6), 1.5)
        self.assertEqual(MathUtil.round_to_nearest_half(1.6, floor=True), 1.5)
        self.assertEqual(MathUtil.round_to_nearest_half(1.6, ceil=True), 2)

        self.assertEqual(MathUtil.round_to_nearest_half(1.4), 1.5)
        self.assertEqual(MathUtil.round_to_nearest_half(1.4, floor=True), 1.0)
        self.assertEqual(MathUtil.round_to_nearest_half(1.4, ceil=True), 1.5)
