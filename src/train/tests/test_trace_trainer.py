from copy import deepcopy
from typing import Dict

import mock

from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager
from train.metrics.metrics_manager import MetricsManager
from train.trace_output.stage_eval import Metrics
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestTraceTrainer(BaseTraceTest):
    VALIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3
    TARGET_LAYERS = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET])
    SOURCE_LAYERS = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE])

    EXPECTED_PREDICTION_SIZE = len(TARGET_LAYERS) * len(SOURCE_LAYERS)
    TEST_METRIC_DEFINITION = [["accuracy", ["accuracy"]], ["map", ["map"]], ["map_at_k", ["map@1", "map@2", "map@3"]],
                              ["f", ["f1", "f2"]]]
    TEST_METRICS_NAMES = [m for m, aliases in TEST_METRIC_DEFINITION]

    def test_perform_training(self):
        test_trace_trainer = self.get_custom_trace_trainer(metrics=self.TEST_METRICS_NAMES)
        test_trace_trainer.model_manager.get_tokenizer().padding = True
        train_output = test_trace_trainer.perform_training()
        self.assertGreater(train_output.training_loss, 0)

    def test_perform_prediction(self):
        test_trace_trainer = self.get_custom_trace_trainer(dataset_container_args={"val_dataset_creator": None},
                                                           metrics=self.TEST_METRICS_NAMES)
        trace_prediction_output = test_trace_trainer.perform_prediction()
        trace_prediction_job_result = JobResult.from_trace_output(trace_prediction_output)
        eval_dataset = test_trace_trainer.trainer_dataset_manager[DatasetRole.EVAL]
        TestAssertions.verify_prediction_output(self, trace_prediction_job_result, eval_dataset)

    def test_perform_prediction_with_metrics(self):
        test_trace_trainer = self.get_custom_trace_trainer(metrics=self.TEST_METRICS_NAMES)
        prediction_output = test_trace_trainer.perform_prediction()
        self.assert_metrics(prediction_output.metrics)

    def test_output_to_dict(self):
        trace_output = TracePredictionOutput(TestDataManager.EXAMPLE_PREDICTION_OUTPUT)
        output_dict = trace_output.output_to_dict()
        self.assertIsInstance(output_dict, dict)
        self.assertIn("predictions", output_dict)
        self.assertIn("label_ids", output_dict)
        self.assertIn("metrics", output_dict)

    def test_eval(self):
        output = deepcopy(TestDataManager.EXAMPLE_PREDICTION_OUTPUT)
        test_trace_trainer = self.get_custom_trace_trainer(metrics=self.TEST_METRICS_NAMES)
        metrics_manager = MetricsManager(test_trace_trainer.trainer_dataset_manager[DatasetRole.EVAL].links.values(),
                                         output.predictions)
        eval_metrics = metrics_manager.eval(self.TEST_METRICS_NAMES)
        self.assert_metrics(eval_metrics)

    def set_train_dataset(self, test_trace_trainer):
        train_dataset = self.create_trainer_dataset_manager()[DatasetRole.TRAIN]
        test_trace_trainer.train_dataset = train_dataset

    def get_custom_trace_trainer(self, dataset_container_args: Dict = None, **kwargs):
        trainer_dataset_manager = self.create_trainer_dataset_manager(dataset_container_args)
        model_manager = ObjectCreator.create(ModelManager)
        model_manager.get_model = mock.MagicMock(return_value=self.get_test_model())
        model_manager.get_tokenizer = mock.MagicMock(return_value=self.get_test_tokenizer())
        model_manager.get_config = mock.MagicMock(return_value=self.get_test_config())
        trainer_args = ObjectCreator.create(TrainerArgs, **kwargs)
        return TraceTrainer(
            trainer_args=trainer_args,
            trainer_dataset_manager=trainer_dataset_manager,
            model_manager=model_manager)

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
            "val_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": .3
            },
            **kwargs
        })
