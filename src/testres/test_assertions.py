from typing import Dict, List, Tuple
from unittest import TestCase

import pandas as pd

from data.datasets.trace_dataset import TraceDataset
from jobs.components.job_result import JobResult
from testres.test_data_manager import TestDataManager
from util.dataframe_util import DataFrameUtil
from util.json_util import JsonUtil


class TestAssertions:
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"

    @classmethod
    def verify_prediction_output(cls, test_case: TestCase, output: JobResult, test_project: TraceDataset) -> None:
        """
        Verifies that prediction output contains correctly formatted predictions and metrics.
        :param test_case: The test case used for making assertions.
        :param output: The output of the prediction job.
        :param test_project: The test project that was being predicted on.
        :return: None
        """
        cls.verify_predictions(test_case, output, test_project)
        cls.verify_metrics_output(test_case, output)

    @classmethod
    def verify_predictions(cls, test_case: TestCase, output: JobResult, eval_dataset: TraceDataset,
                           base_score: float = 0.5, threshold=0.3) -> None:
        """
        Verifies that output contains predictions matching data in evaluation dataset.
        :param test_case: The test case to make assertions with.
        :param output: The output of a prediction job.
        :param eval_dataset: The evaluation dataset used in prediction job.
        :param base_score: The base score that other scores are expected to be a threshold away from.
        :param threshold: The tolerance threshold between score and base score.
        :return: None
        """
        output.require_properties([JobResult.PREDICTIONS])
        predictions = output[JobResult.PREDICTIONS]
        test_case.assertEqual(len(eval_dataset), len(predictions))

        expected_keys = [JobResult.SOURCE, JobResult.TARGET, JobResult.SCORE]
        for prediction in predictions:
            JsonUtil.require_properties(prediction, expected_keys)
            score = prediction[JobResult.SCORE]
            if abs(score - base_score) >= threshold:
                test_case.fail(cls._VAL_ERROR_MESSAGE.format(JobResult.SCORE, score, base_score, JobResult.PREDICTIONS))

        predicted_links: List[Tuple[str, str]] = [(p[JobResult.SOURCE], p[JobResult.TARGET]) for p in predictions]
        expected_links: List[Tuple[str, str]] = eval_dataset.get_source_target_pairs()
        cls.assert_lists_have_the_same_vals(test_case, expected_links, predicted_links)

    @classmethod
    def verify_metrics_output(cls, test_case: TestCase, output: JobResult) -> None:
        """
        Verifies that prediction job result contains valid metric results.
        :param test_case: The test case used to make assertions.
        :param output: The result of a prediction job.
        :return: None
        """
        output.require_properties([JobResult.METRICS])
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
        for entity in expected_entities:
            query_df = DataFrameUtil.query_df(entity_df, entity)
            test_case.assertEquals(1, len(query_df), msg=f"Could not find row with: {entity}")
