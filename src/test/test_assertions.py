from unittest import TestCase

from jobs.components.job_result import JobResult
from test.test_data_manager import TestDataManager


class TestAssertions:
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"

    def assert_prediction_output_matches_expected(self, test_case: TestCase, output: dict, threshold: int = 0.05):
        if JobResult.PREDICTIONS not in output:
            test_case.fail(self._KEY_ERROR_MESSAGE.format(JobResult.PREDICTIONS, output))
        predictions = output[JobResult.PREDICTIONS]
        all_links = TestDataManager.get_all_links()
        if len(predictions) != len(all_links):
            test_case.fail(self._LEN_ERROR.format(JobResult.PREDICTIONS))
        expected_links = {link for link in all_links}
        predicted_links = set()
        for link_dict in output[JobResult.PREDICTIONS]:
            link = [None, None]
            for key, val in TestDataManager.EXAMPLE_PREDICTION_LINKS.items():
                if key not in link_dict:
                    test_case.fail(self._KEY_ERROR_MESSAGE.format(key, JobResult.PREDICTIONS))
                if key == "score":
                    expected_val = TestDataManager.EXAMPLE_PREDICTION_LINKS["score"]
                    if abs(val - expected_val) >= threshold:
                        test_case.fail(
                            self._VAL_ERROR_MESSAGE.format(key, val, expected_val, JobResult.PREDICTIONS))
                else:
                    link[val] = link_dict[key]
            predicted_links.add(tuple(link))
        self.assert_lists_have_the_same_vals(test_case, expected_links, predicted_links)
        if JobResult.METRICS not in output:
            test_case.fail(self._KEY_ERROR_MESSAGE.format(JobResult.METRICS, output))
        for metric in TestDataManager.EXAMPLE_PREDICTION_METRICS.keys():
            if metric not in output[JobResult.METRICS]:
                test_case.fail(
                    self._KEY_ERROR_MESSAGE.format(JobResult.METRICS, output[JobResult.METRICS]))

    @staticmethod
    def assert_training_output_matches_expected(test_case: TestCase, output_dict: dict):
        for key, value in TestDataManager.EXAMPLE_TRAINING_OUTPUT.items():
            test_case.assertIn(key, output_dict)

    @staticmethod
    def assert_lists_have_the_same_vals(test_case: TestCase, list1, list2):
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        test_case.assertEquals(len(diff1), 0)
        test_case.assertEquals(len(diff2), 0)
