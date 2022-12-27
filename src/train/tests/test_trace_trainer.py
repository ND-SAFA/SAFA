from copy import deepcopy
from unittest.mock import patch

import mock
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.predict_job import PredictJob
from models.model_manager import ModelManager
from test.base_trace_test import BaseTraceTest
from test.test_assertions import TestAssertions
from test.test_data_manager import TestDataManager
from test.test_object_creator import TestObjectCreator
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.variables.typed_definition_variable import TypedDefinitionVariable


class TestTraceTrainer(BaseTraceTest):
    VALIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3
    TARGET_LAYERS = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET])
    SOURCE_LAYERS = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE])

    EXPECTED_PREDICTION_SIZE = len(TARGET_LAYERS) * len(SOURCE_LAYERS)
    TEST_METRIC_NAMES = ["accuracy", "map"]

    def test_perform_training(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        test_trace_trainer.model_manager.get_tokenizer().padding = True
        output = test_trace_trainer.perform_training()
        self.assertIn("training_loss", output)

    def test_perform_prediction(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        output = test_trace_trainer.perform_prediction()
        output = PredictJob._result_from_prediction_output(output)
        TestAssertions.assert_prediction_output_matches_expected(self, output.as_dict())

    def test_perform_prediction_with_metrics(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        output = test_trace_trainer.perform_prediction()
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, output["metrics"])

    def test_output_to_dict(self):
        output_dict = TraceTrainer.output_to_dict(TestDataManager.EXAMPLE_PREDICTION_OUTPUT)
        self.assertIsInstance(output_dict, dict)
        self.assertIn("predictions", output_dict)
        self.assertIn("label_ids", output_dict)
        self.assertIn("metrics", output_dict)

    def test_eval(self):
        output = deepcopy(TestDataManager.EXAMPLE_PREDICTION_OUTPUT)
        result = TraceTrainer._eval(output.predictions, output.label_ids, output.metrics, self.TEST_METRIC_NAMES)
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, result)

    @patch("torch.distributed.get_rank")
    @patch("torch.distributed.get_world_size")
    def test_get_train_dataloader_local_rank_not_neg_one(self, get_world_size_mock: mock.MagicMock,
                                                         get_rank_mock: mock.MagicMock):
        get_world_size_mock.return_value = 5
        get_rank_mock.return_value = 3
        test_trace_trainer = self.get_test_trace_trainer()
        self.set_train_dataset(test_trace_trainer)
        test_trace_trainer.trainer_args.local_rank = 2
        data_loader = test_trace_trainer.get_train_dataloader()
        self.assertIsInstance(data_loader.sampler, DistributedSampler)

    def test_get_train_dataloader_local_rank_neg_one(self):
        test_trace_trainer = self.get_test_trace_trainer()
        self.set_train_dataset(test_trace_trainer)
        test_trace_trainer.trainer_args.local_rank = -1
        data_loader = test_trace_trainer.get_train_dataloader()
        self.assertIsInstance(data_loader.sampler, RandomSampler)

    def set_train_dataset(self, test_trace_trainer):
        train_dataset = self.get_dataset_container()[DatasetRole.TRAIN]
        test_trace_trainer.train_dataset = train_dataset

    def get_test_trace_trainer(self, **kwargs):
        trainer_dataset_manager = self.get_dataset_container()
        model_manager = TestObjectCreator.create(ModelManager)
        model_manager.get_model = mock.MagicMock(return_value=self.get_test_model())
        model_manager.get_tokenizer = mock.MagicMock(return_value=self.get_test_tokenizer())
        trainer_args = TestObjectCreator.create(TrainerArgs, **kwargs)
        return TraceTrainer(
            trainer_args=trainer_args,
            trainer_dataset_manager=trainer_dataset_manager,
            model_manager=model_manager)

    @staticmethod
    def get_dataset_container():
        return TestObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "CLASSIC_TRACE",
                **TestObjectCreator.dataset_creator_definition
            },
            "val_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": .3
            }
        })
