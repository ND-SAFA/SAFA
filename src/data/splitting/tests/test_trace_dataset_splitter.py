from unittest import mock
from unittest.mock import patch

from data.splitting.tests.base_split_test import BaseSplitTest
from data.splitting.trace_dataset_splitter import TraceDatasetSplitter
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest


class TestTraceDatasetSplitter(BaseSplitTest):
    """
    Responsible for testing trace dataset splitter under default functionality ensuring
    that splits contain the right sizes.
    """

    @patch.object(ModelManager, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        splitter = TraceDatasetSplitter(self.get_trace_dataset())
        train_dataset, test_dataset = splitter.split(self.VAlIDATION_PERCENTAGE)
        train_dataset.prepare_for_training()
        model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
        trainer_dataset = train_dataset.to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(trainer_dataset[0], dict))
        self.assertEquals(self.get_expected_train_dataset_size(resample_rate=1), len(trainer_dataset))

    def get_expected_train_dataset_size(self, resample_rate=BaseTraceTest.RESAMPLE_RATE,
                                        validation_percentage=BaseTraceTest.VAlIDATION_PERCENTAGE):
        num_train_pos_links = round(self.N_POSITIVE * (1 - validation_percentage))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links
