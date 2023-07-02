from tgen.data.processing.cleaning.filter_min_length_step import FilterMinLengthStep
from tgen.testres.base_tests.base_test import BaseTest


class TestFilterMinLengthStep(BaseTest):
    TEST_WORD_LIST = "This is a test".split()

    def test_run(self):
        step_min_length_1 = self.get_test_step()
        result1 = step_min_length_1.run(self.TEST_WORD_LIST)
        self.assertEqual(result1, "This is test".split())

        step_min_length_2 = self.get_test_step(2)
        result2 = step_min_length_2.run(self.TEST_WORD_LIST)
        self.assertEqual(result2, "This test".split())

    def get_test_step(self, min_length=1):
        return FilterMinLengthStep(min_length)
