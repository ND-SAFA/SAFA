from copy import deepcopy
from unittest.mock import patch

import mock
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler

from test.base_trace_test import BaseTraceTest
from tracer.dataset.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.dataset.trainer_datasets_container import TrainerDatasetsContainer
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.models.model_generator import ModelGenerator
from tracer.train.trace_args import TraceArgs
from tracer.train.trace_trainer import TraceTrainer


class TestTraceTrainer(BaseTraceTest):
    VALIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3
    EXPECTED_PREDICTION_SIZE = len(BaseTraceTest.TARGET_LAYERS) * len(BaseTraceTest.SOURCE_LAYERS)
    TEST_METRIC_NAMES = ["accuracy", "map_at_k"]

    def test_perform_training(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        test_trace_trainer.model_generator.get_tokenizer().padding = True
        output = test_trace_trainer.perform_training()
        self.assertIn("training_loss", output)

    @patch.object(TraceTrainer, "_eval")
    def test_perform_prediction(self, eval_mock: mock.MagicMock):
        test_trace_trainer = self.get_test_trace_trainer()
        output = test_trace_trainer.perform_prediction()
        self.assert_prediction_output_matches_expected(output)
        self.assertFalse(eval_mock.called)

    def test_perform_prediction_with_metrics(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        output = test_trace_trainer.perform_prediction()
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, output["metrics"])

    def test_output_to_dict(self):
        output_dict = TraceTrainer.output_to_dict(self.EXAMPLE_PREDICTION_OUTPUT)
        self.assertIsInstance(output_dict, dict)
        self.assertIn("predictions", output_dict)
        self.assertIn("label_ids", output_dict)
        self.assertIn("metrics", output_dict)

    def test_eval(self):
        output = deepcopy(self.EXAMPLE_PREDICTION_OUTPUT)
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
        test_trace_trainer.train_dataset = self.get_dataset_contianer().train_dataset

    def get_dataset_contianer(self):
        dataset_map_train = self.create_dataset_map(DatasetRole.TRAIN, include_links=True)
        dataset_map_eval = self.create_dataset_map(DatasetRole.EVAL, include_links=False)
        return self.create_trainer_dataset_container({**dataset_map_train, **dataset_map_eval},
                                                     split_train_dataset=True)

    def get_test_trace_trainer(self, **kwargs):
        trainer_dataset_container = self.get_dataset_contianer()
        model_generator = ModelGenerator(SupportedBaseModel.PL_BERT, "path")
        model_generator.get_model = mock.MagicMock(return_value=self.get_test_model())
        model_generator.get_tokenizer = mock.MagicMock(return_value=self.get_test_tokenizer())
        return TraceTrainer(TraceArgs(output_dir="output", trainer_dataset_container=trainer_dataset_container, **kwargs),
                            model_generator)
