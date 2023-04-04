from unittest import mock
from unittest.mock import patch

from tgen.datasets import Dataset

from tgen.data.tdatasets.pre_train_dataset import PreTrainDataset
from tgen.models.model_manager import ModelManager
from test.testres.base_test import BaseTest
from test.testres.paths.paths import TEST_VOCAB_FILE


class TestPreTrainDataset(BaseTest):

    @patch.object(ModelManager, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
        dataset = self.get_pre_train_dataset()
        dataset = dataset.to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(dataset, Dataset))

    def get_pre_train_dataset(self):
        return PreTrainDataset(TEST_VOCAB_FILE, block_size=128)
