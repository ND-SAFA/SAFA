from typing import Dict, List, Tuple
from unittest import TestCase

import pandas as pd
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.objects.trace_layer import TraceLayer
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.json_util import JsonUtil
from common_resources.tools.util.status import Status

from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.jobs.components.job_result import JobResult
from tgen.testres.test_data_manager import TestDataManager


class TestAssertions:
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"

    @classmethod
    def verify_prediction_output(cls, test_case: TestCase, output: JobResult, test_project: TraceDataset,
                                 base_score: float = 0.5) -> None:
        """
        Verifies that prediction output contains correctly formatted predictions and metrics.
        :param test_case: The test case used for making assertions.
        :param output: The output of the prediction job.
        :param test_project: The test project that was being predicted on.
        :param base_score: The base score that other scores are expected to be a threshold away from.
        :return: None
        """
        cls.verify_predictions(test_case, output, test_project, base_score)
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
        if isinstance(output, JobResult):
            output = output.body
        if isinstance(output, TraceTrainOutput):
            output = output.prediction_output
        prediction_entries = output.prediction_entries
        test_case.assertEqual(len(eval_dataset), len(prediction_entries))

        expected_keys = ["source", "target", "score"]  # todo: replace with reflection
        for prediction_entry in prediction_entries:
            JsonUtil.require_properties(prediction_entry, expected_keys)
            score = prediction_entry["score"]
            if abs(score - base_score) >= threshold:
                test_case.fail(cls._VAL_ERROR_MESSAGE.format("score", score, base_score, "predictions"))

        predicted_links: List[Tuple[str, str]] = [(p["source"], p["target"]) for p in prediction_entries]
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
        if isinstance(output, JobResult):
            output = output.body
        if isinstance(output, TraceTrainOutput):
            output = output.prediction_output
        if not isinstance(output, TracePredictionOutput) and isinstance(output, dict):
            output = TracePredictionOutput(**output)
        for metric in TestDataManager.EXAMPLE_PREDICTION_METRICS.keys():
            if metric not in output.metrics:
                test_case.fail(
                    cls._KEY_ERROR_MESSAGE.format(metric, output.metrics))

    @staticmethod
    def assert_training_output_matches_expected(test_case: TestCase, job_result: JobResult, expected_output=None):
        expected_output = expected_output if expected_output else TestDataManager.EXAMPLE_TRAINING_OUTPUT
        if "status" in expected_output:
            expected_output.pop("status")
            test_case.assertEqual(job_result.status, Status.SUCCESS)
        output = job_result.body
        if isinstance(output, AbstractTraceOutput):
            output = output.output_to_dict()
        for key, value in expected_output.items():
            test_case.assertIsNotNone(output.get(key, None))

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
        test_case.assertEqual(len(diff1), 0)
        test_case.assertEqual(len(diff2), 0)

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
            test_case.assertEqual(1, len(query_df), msg=f"Could not find row with: {entity}")

    @staticmethod
    def verify_row_contains(test_case: TestCase, row: pd.Series, properties: Dict, delta=0.01) -> None:
        """
        Verifies that row contains properties within delta range.
        :param test_case: The test case used to make assertions.
        :param row: The row whose properties are checked.
        :param properties: The properties to assert in row.
        :param delta: The allowable delta between comparisons.
        :return: None
        """
        for k, v in properties.items():
            test_case.assertAlmostEqual(v, row[k], delta=delta)

    @staticmethod
    def verify_trace_layers(test_case: TestCase, trace_layers: List[TraceLayer], layer_df: LayerDataFrame) -> None:
        """
        Verifies that trace layers are present in layer data frame.
        :param test_case: The test case to make assertions for.
        :param trace_layers: The expected trace layers in the data frame.
        :param layer_df: The data frame mapping taced layers.
        :return: None
        """
        layer_dicts = [{"source_type": l.child, "target_type": l.parent} for l in trace_layers]
        TestAssertions.verify_entities_in_df(test_case, layer_dicts, layer_df)
