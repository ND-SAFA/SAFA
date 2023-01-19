from typing import Dict, List
from unittest import TestCase

import pandas as pd

from jobs.components.job_result import JobResult
from testres.test_data_manager import TestDataManager
from testres.testprojects.api_test_project import ApiTestProject


class TestAssertions:
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"

    @classmethod
    def assert_prediction_output_matches_expected(cls, test_case: TestCase, output: dict, threshold: int = 0.05):
        if JobResult.PREDICTIONS not in output:
            test_case.fail(cls._KEY_ERROR_MESSAGE.format(JobResult.PREDICTIONS, output))
        predictions = output[JobResult.PREDICTIONS]
        all_links = TestDataManager.get_all_links()
        test_case.assertEquals(len(predictions), ApiTestProject.get_n_links(), cls._LEN_ERROR.format(JobResult.PREDICTIONS))
        expected_links = {link for link in all_links}
        predicted_links = set()
        for link_dict in output[JobResult.PREDICTIONS]:
            link = [None, None]
            for key, val in TestDataManager.EXAMPLE_PREDICTION_LINKS.items():
                if key not in link_dict:
                    test_case.fail(cls._KEY_ERROR_MESSAGE.format(key, JobResult.PREDICTIONS))
                if key == "score":
                    expected_val = TestDataManager.EXAMPLE_PREDICTION_LINKS["score"]
                    if abs(val - expected_val) >= threshold:
                        test_case.fail(
                            cls._VAL_ERROR_MESSAGE.format(key, val, expected_val, JobResult.PREDICTIONS))
                else:
                    link[val] = link_dict[key]
            predicted_links.add(tuple(link))
        cls.assert_lists_have_the_same_vals(test_case, expected_links, predicted_links)
        if JobResult.METRICS not in output:
            test_case.fail(cls._KEY_ERROR_MESSAGE.format(JobResult.METRICS, output))
        for metric in TestDataManager.EXAMPLE_PREDICTION_METRICS.keys():
            if metric not in output[JobResult.METRICS]:
                test_case.fail(
                    cls._KEY_ERROR_MESSAGE.format(metric, output[JobResult.METRICS]))

    @staticmethod
    def assert_training_output_matches_expected(test_case: TestCase, output_dict: dict, expected_output=None):
        expected_output = expected_output if expected_output else TestDataManager.EXAMPLE_TRAINING_OUTPUT
        for key, value in expected_output.items():
            test_case.assertIn(key, output_dict)

    @staticmethod
    def assert_lists_have_the_same_vals(test_case: TestCase, list1, list2) -> None:
        """
        Tests that list items are identical in both lists.
        :param test_case: The test to use for assertions.
        :param list1: One of the lists to compare.
        :param list2: The other list to compare.
        :return: None
        """
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        test_case.assertEquals(len(diff1), 0)
        test_case.assertEquals(len(diff2), 0)

    @staticmethod
    def verify_entities_in_df(test_case: TestCase, expected_entities: List[Dict], entity_df: pd.DataFrame, **kwargs) -> None:
        """
        Verifies that each data frame contains entities given.
        :param test_case: The test case used to verify result.
        :param entity_df: The data frame expected to contain entities
        :param expected_entities: The entities to verify exist in data frame
        :param kwargs: Any additional parameters to assertion function
        :return: None
        """
        test_case.assertEqual(len(expected_entities), len(entity_df))
        for row_index, row in entity_df.iterrows():
            entity = expected_entities[row_index]
            for param_name, param_value in entity.items():
                assert param_name in row, f"{row.to_dict()} does not contain: {param_name}"
                error_message = f"Row: {row.to_dict()} | Param: {param_name}"
                test_case.assertEqual(param_value, row[param_name], msg=error_message)
