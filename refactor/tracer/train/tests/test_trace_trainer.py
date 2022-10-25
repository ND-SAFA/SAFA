from copy import deepcopy
from unittest.mock import patch

import mock
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler

from test.base_test import BaseTest
from tracer.dataset.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.models.model_generator import ModelGenerator
from tracer.train.trace_args import TraceArgs
from tracer.train.trace_trainer import TraceTrainer


class TestTraceTrainer(BaseTest):
    VALIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3
    EXPECTED_PREDICTION_SIZE = len(BaseTest.TEST_TARGET_LAYERS) * len(BaseTest.TEST_SOURCE_LAYERS)
    TEST_METRIC_NAMES = ["accuracy", "map_at_k"]

    def test_perform_training(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        test_trace_trainer.model_generator.get_tokenizer().padding = True
        train_dataset, eval_dataset = self.get_dataset().split(self.VALIDATION_PERCENTAGE)
        output = test_trace_trainer.perform_training(train_dataset, eval_dataset)
        self.assertIn("training_loss", output)

    @patch.object(TraceTrainer, "_eval")
    def test_perform_prediction(self, eval_mock: mock.MagicMock):
        test_trace_trainer = self.get_test_trace_trainer()
        output = test_trace_trainer.perform_prediction(self.get_dataset(include_links=False))
        self.assert_output_matches_expected(output)
        self.assertFalse(eval_mock.called)

    def test_perform_prediction_with_metrics(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        output = test_trace_trainer.perform_prediction(self.get_dataset(include_links=False))
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, output["metrics"])

    def test_output_to_dict(self):
        output_dict = TraceTrainer.output_to_dict(self.TEST_PREDICTION_OUTPUT)
        self.assertIsInstance(output_dict, dict)
        self.assertIn("predictions", output_dict)
        self.assertIn("label_ids", output_dict)
        self.assertIn("metrics", output_dict)

    def test_eval(self):
        output = deepcopy(self.TEST_PREDICTION_OUTPUT)
        TraceTrainer._eval(output.predictions, output.label_ids, self.TEST_METRIC_NAMES)
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, output.metrics)

    @patch("torch.distributed.get_rank")
    @patch("torch.distributed.get_world_size")
    def test_get_train_dataloader_local_rank_not_neg_one(self, get_world_size_mock: mock.MagicMock,
                                                         get_rank_mock: mock.MagicMock):
        get_world_size_mock.return_value = 5
        get_rank_mock.return_value = 3
        test_trace_trainer = self.get_test_trace_trainer()
        self.set_train_dataset(test_trace_trainer)
        test_trace_trainer.args.local_rank = 2
        data_loader = test_trace_trainer.get_train_dataloader()
        self.assertIsInstance(data_loader.sampler, DistributedSampler)

    def test_get_train_dataloader_local_rank_neg_one(self):
        test_trace_trainer = self.get_test_trace_trainer()
        self.set_train_dataset(test_trace_trainer)
        test_trace_trainer.args.local_rank = -1
        data_loader = test_trace_trainer.get_train_dataloader()
        self.assertIsInstance(data_loader.sampler, RandomSampler)

    def set_train_dataset(self, test_trace_trainer):
        test_trace_trainer.train_dataset = self.get_dataset()

    def get_dataset(self, include_links=True):
        return ClassicTraceDatasetCreator(self.TEST_SOURCE_LAYERS, self.TEST_TARGET_LAYERS,
                                          true_links=self.TEST_POS_LINKS if include_links else None).create()

    def get_test_trace_trainer(self, **kwargs):
        model_generator = ModelGenerator(SupportedBaseModel.PL_BERT, "path")
        model_generator.get_model = mock.MagicMock(return_value=self.get_test_model())
        model_generator.get_tokenizer = mock.MagicMock(return_value=self.get_test_tokenizer())
        return TraceTrainer(TraceArgs(output_dir="output", **kwargs), model_generator)
