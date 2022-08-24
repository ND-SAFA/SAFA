from copy import copy, deepcopy

from django.test import TestCase

from unittest.mock import patch
import mock

from common.models.model_generator import ModelGenerator
from test.config.paths import TEST_OUTPUT_DIR
from test.test_data import TEST_S_ARTS, TEST_T_ARTS, TEST_POS_LINKS
from test.test_model import get_test_model
from test.test_tokenizer import get_test_tokenizer
from trace.data.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs
from trace.train.trace_trainer import TraceTrainer
import numpy as np

from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler
from transformers.trainer_utils import PredictionOutput


class TestTraceTrainer(TestCase):
    VAlIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3
    EXPECTED_PREDICTION_SIZE = len(TEST_T_ARTS) * len(TEST_S_ARTS)
    TEST_METRIC_NAMES = ["accuracy", "map_at_k"]
    TEST_METRIC_RESULTS = {'test_loss': 0.6929082870483398}
    TEST_PREDICTIONS = np.array([[0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124]])
    TEST_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
    TEST_PREDICTION_OUTPUT = PredictionOutput(predictions=TEST_PREDICTIONS,
                                              label_ids=TEST_LABEL_IDS,
                                              metrics=TEST_METRIC_RESULTS)

    @patch.object(TraceTrainer, "save_model")
    def test_perform_training(self, save_model_mock: mock.MagicMock):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        test_trace_trainer.model_generator.get_tokenizer().padding = True
        output = test_trace_trainer.perform_training()
        self.assertTrue(save_model_mock.called)
        self.assertIn("training_loss", output)

    @patch.object(TraceTrainer, "_eval")
    def test_perform_prediction(self, eval_mock: mock.MagicMock):
        test_trace_trainer = self.get_test_trace_trainer()
        output = test_trace_trainer.perform_prediction()
        self.assertEquals(len(output["predictions"]), self.EXPECTED_PREDICTION_SIZE)
        self.assertEquals(len(output[test_trace_trainer.args.prediction_ids_key]), len(output["predictions"]))
        self.assertFalse(eval_mock.called)

    def test_perform_prediction_with_metrics(self):
        test_trace_trainer = self.get_test_trace_trainer(metrics=self.TEST_METRIC_NAMES)
        output = test_trace_trainer.perform_prediction()
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
        TraceTrainer._eval(output, self.TEST_METRIC_NAMES)
        for metric in self.TEST_METRIC_NAMES:
            self.assertIn(metric, output.metrics)

    @patch("torch.distributed.get_rank")
    @patch("torch.distributed.get_world_size")
    def test_get_train_dataloader_local_rank_not_neg_one(self, get_world_size_mock: mock.MagicMock, get_rank_mock: mock.MagicMock):
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
        test_trace_trainer.train_dataset = test_trace_trainer.trace_dataset_creator.get_training_dataset(1)

    def get_test_trace_trainer(self, args=None, **kwargs):
        if args is None:
            model_generator = ModelGenerator("bert_trace_single", "path")
            model_generator.get_model = mock.MagicMock(return_value=get_test_model())
            model_generator.get_tokenizer = mock.MagicMock(return_value=get_test_tokenizer())
            trace_dataset_creator = TraceDatasetCreator(source_artifacts=TEST_S_ARTS, target_artifacts=TEST_T_ARTS,
                                                        true_links=TEST_POS_LINKS,
                                                        model_generator=model_generator,
                                                        validation_percentage=self.VAlIDATION_PERCENTAGE)
            args = TraceArgs(model_generator=model_generator,
                             trace_dataset_creator=trace_dataset_creator,
                             output_path=TEST_OUTPUT_DIR, **kwargs)
        return TraceTrainer(args)
