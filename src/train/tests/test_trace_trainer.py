import os
from copy import deepcopy
from typing import Dict
from unittest.mock import patch

import mock
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager
from train.metrics.metrics_manager import MetricsManager
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
    TEST_METRIC_NAMES = ["accuracy", "map"]

    def test_perform_training(self):
        test_trace_trainer = self.get_custom_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        test_trace_trainer.model_manager.get_tokenizer().padding = True
        train_output = test_trace_trainer.perform_training()
        self.assertGreater(train_output.training_loss, 0)

    def test_perform_prediction(self):
        test_trace_trainer = self.get_custom_trace_trainer(dataset_container_args={"val_dataset_creator": None},
                                                           metrics=self.TEST_METRIC_NAMES)
        trace_prediction_output = test_trace_trainer.perform_prediction()
        trace_prediction_job_result = JobResult.from_trace_output(trace_prediction_output)
        eval_dataset = test_trace_trainer.trainer_dataset_manager[DatasetRole.EVAL]
        TestAssertions.verify_prediction_output(self, trace_prediction_job_result, eval_dataset)

    def test_perform_prediction_with_metrics(self):
        test_trace_trainer = self.get_custom_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        output = test_trace_trainer.perform_prediction()
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, output.metrics)

    def test_output_to_dict(self):
        trace_output = TracePredictionOutput(TestDataManager.EXAMPLE_PREDICTION_OUTPUT)
        output_dict = trace_output.output_to_dict()
        self.assertIsInstance(output_dict, dict)
        self.assertIn("predictions", output_dict)
        self.assertIn("label_ids", output_dict)
        self.assertIn("metrics", output_dict)

    def test_eval(self):
        output = deepcopy(TestDataManager.EXAMPLE_PREDICTION_OUTPUT)
        test_trace_trainer = self.get_custom_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        metrics_manager = MetricsManager(test_trace_trainer.trainer_dataset_manager[DatasetRole.EVAL].links.values(),
                                         output.predictions)
        result = metrics_manager.eval(self.TEST_METRIC_NAMES)
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, result)

    @patch("torch.distributed.get_rank")
    @patch("torch.distributed.get_world_size")
    def test_get_train_dataloader_local_rank_not_neg_one(self, get_world_size_mock: mock.MagicMock,
                                                         get_rank_mock: mock.MagicMock):
        get_world_size_mock.return_value = 5
        get_rank_mock.return_value = 3
        test_trace_trainer = self.get_custom_trace_trainer()
        self.set_train_dataset(test_trace_trainer)
        test_trace_trainer.trainer_args.local_rank = 2
        data_loader = test_trace_trainer.get_train_dataloader()
        self.assertIsInstance(data_loader.sampler, DistributedSampler)

    def test_get_train_dataloader_local_rank_neg_one(self):
        test_trace_trainer = self.get_custom_trace_trainer()
        self.set_train_dataset(test_trace_trainer)
        test_trace_trainer.trainer_args.local_rank = -1
        data_loader = test_trace_trainer.get_train_dataloader()
        self.assertIsInstance(data_loader.sampler, RandomSampler)

    def set_train_dataset(self, test_trace_trainer):
        train_dataset = self.create_trainer_dataset_manager()[DatasetRole.TRAIN]
        test_trace_trainer.train_dataset = train_dataset

    def get_custom_trace_trainer(self, dataset_container_args: Dict = None, **kwargs):
        trainer_dataset_manager = self.create_trainer_dataset_manager(dataset_container_args)
        model_manager = ObjectCreator.create(ModelManager)
        model_manager.get_model = mock.MagicMock(return_value=self.get_test_model())
        model_manager.get_tokenizer = mock.MagicMock(return_value=self.get_test_tokenizer())
        trainer_args = ObjectCreator.create(TrainerArgs, **kwargs)
        return TraceTrainer(
            trainer_args=trainer_args,
            trainer_dataset_manager=trainer_dataset_manager,
            model_manager=model_manager)

    def test_save_checkpoint(self):
        test_trace_trainer = self.get_custom_trace_trainer()
        test_trace_trainer.perform_training()
        checkpoint_files = ["optimizer.bin", "config.json", "pytorch_model.bin", "scheduler.bin",
                            "training_args.bin"]
        for folder_name in [TraceTrainer.BEST_MODEL_NAME, TraceTrainer.CURRENT_MODEL_NAME]:
            folder_path = os.path.join(test_trace_trainer.trainer_args.output_dir, folder_name)
            output_files = list(os.listdir(folder_path))
            for file in checkpoint_files:
                self.assertIn(file, output_files)

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
