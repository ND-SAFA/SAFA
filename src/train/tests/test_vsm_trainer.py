from typing import Dict
from unittest import mock

from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_result import JobResult
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager
from train.trace_output.stage_eval import Metrics
from train.vsm_trainer import VSMTrainer
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestVSMTrainer(BaseTraceTest):
    TARGET_LAYERS = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET])
    SOURCE_LAYERS = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE])

    EXPECTED_PREDICTION_SIZE = len(TARGET_LAYERS) * len(SOURCE_LAYERS)
    TEST_METRIC_DEFINITION = [["accuracy", ["accuracy"]], ["map", ["map"]], ["map_at_k", ["map@1", "map@2", "map@3"]],
                              ["f", ["f1", "f2"]]]
    TEST_METRICS_NAMES = [m for m, aliases in TEST_METRIC_DEFINITION]

    def test_perform_prediction(self):
        test_trace_trainer = self.get_custom_trace_trainer(dataset_container_args={"val_dataset_creator": None})
        test_trace_trainer.perform_training()
        trace_prediction_output = test_trace_trainer.perform_prediction(metrics=self.TEST_METRICS_NAMES)
        trace_prediction_job_result = JobResult.from_trace_output(trace_prediction_output)
        eval_dataset = test_trace_trainer.trainer_dataset_manager[DatasetRole.EVAL]
        TestAssertions.verify_prediction_output(self, trace_prediction_job_result, eval_dataset, base_score=0.0)
        self.assert_metrics(trace_prediction_output.metrics)

    def get_custom_trace_trainer(self, dataset_container_args: Dict = None):
        trainer_dataset_manager = self.create_trainer_dataset_manager(dataset_container_args)
        return VSMTrainer(trainer_dataset_manager=trainer_dataset_manager)

    def assert_metrics(self, metrics: Metrics):
        """
        Verifies that metrics contains all the desired metrics.
        :param metrics: The metrics object being checked.
        """
        for metric, aliases in self.TEST_METRIC_DEFINITION:
            for alias in aliases:
                self.assertIn(alias, metrics)

    @staticmethod
    def create_trainer_dataset_manager(kwargs: Dict = None) -> TrainerDatasetManager:
        """
        Creates dataset manager with optional kwargs used to modify definition.
        :param kwargs: Dictionary of properties to overwrite in dataset manager definition.
        :return: Dataset manager created.
        """
        if kwargs is None:
            kwargs = {}
        return ObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            },
            **kwargs
        })
