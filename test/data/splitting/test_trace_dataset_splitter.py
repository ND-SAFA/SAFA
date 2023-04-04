from collections import OrderedDict
from unittest import mock
from unittest.mock import patch

from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.splitting.random_split_strategy import RandomSplitStrategy
from tgen.data.splitting.remainder_split_strategy import RemainderSplitStrategy
from tgen.data.splitting.tests.base_split_test import BaseSplitTest
from tgen.data.splitting.dataset_splitter import DatasetSplitter
from tgen.models.model_manager import ModelManager
from test.testres.base_trace_test import BaseTraceTest


class TestTraceDatasetSplitter(BaseSplitTest):
    """
    Responsible for testing trace dataset splitter under default functionality ensuring
    that splits contain the right sizes.
    """

    @patch.object(ModelManager, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        splitter = DatasetSplitter(self.get_trace_dataset(), OrderedDict({DatasetRole.TRAIN: 1-self.VAlIDATION_PERCENTAGE,
                                                              DatasetRole.VAL: self.VAlIDATION_PERCENTAGE}))
        splits = splitter.split_dataset()
        splits[DatasetRole.TRAIN].prepare_for_training()
        model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
        trainer_dataset = splits[DatasetRole.TRAIN].to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(trainer_dataset[0], dict))
        self.assertEquals(self.get_expected_train_dataset_size(resample_rate=1), len(trainer_dataset))

    def get_expected_train_dataset_size(self, resample_rate=BaseTraceTest.RESAMPLE_RATE,
                                        validation_percentage=BaseTraceTest.VAlIDATION_PERCENTAGE):
        num_train_pos_links = round(self.N_POSITIVE * (1 - validation_percentage))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links
