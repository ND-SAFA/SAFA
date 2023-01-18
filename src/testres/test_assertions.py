from typing import Dict, List
from unittest import TestCase

import pandas as pd

from data.datasets.keys.structure_keys import StructureKeys
from jobs.components.job_result import JobResult
from testres.test_data_manager import TestDataManager


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
        test_case.assertEquals(len(predictions), len(all_links), cls._LEN_ERROR.format(JobResult.PREDICTIONS))
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
    def assert_lists_have_the_same_vals(test_case: TestCase, list1, list2):
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        test_case.assertEquals(len(diff1), 0)
        test_case.assertEquals(len(diff2), 0)

    @staticmethod
    def assert_file_definitions_have_files(test_case: TestCase,
                                           artifact_definitions: Dict,
                                           expected_artifact_files: List[str]):
        artifact_files = [artifact_def[StructureKeys.PATH] for artifact_def in artifact_definitions.values()]
        TestAssertions.assert_lists_have_the_same_vals(test_case, artifact_files, expected_artifact_files)

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
                test_case.assertEqual(param_value, row[param_name], **kwargs)
