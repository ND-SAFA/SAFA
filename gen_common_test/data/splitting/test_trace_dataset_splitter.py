from collections import OrderedDict
from unittest import mock
from unittest.mock import patch

from gen_common.data.processing.augmentation.data_augmenter import DataAugmenter
from gen_common.data.processing.augmentation.resample_step import ResampleStep
from gen_common.data.splitting.dataset_splitter import DatasetSplitter
from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.llm.model_manager import ModelManager
from gen_common_test.base_tests.base_split_test import BaseSplitTest
from gen_common_test.base_tests.base_trace_test import BaseTraceTest


class TestTraceDatasetSplitter(BaseSplitTest):
    """
    Responsible for testing trace dataset splitter under default functionality ensuring
    that splits contain the right sizes.
    """
    split_percentages = OrderedDict({DatasetRole.TRAIN: 2 / 3,
                                     DatasetRole.VAL: 1 / 3})
    split_counts = {
        DatasetRole.TRAIN: 16,
        DatasetRole.VAL: 8
    }

    @patch.object(ModelManager, "get_tokenizer")
    def test_to_hf_dataset(self, get_tokenizer_mock: mock.MagicMock):
        """
        Tests correctness of trace entries after splitting and balancing.
        """
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        dataset = self.get_trace_dataset()
        dataset.prepare_for_training()

        splitter = DatasetSplitter(dataset, self.split_percentages)
        splits = splitter.split_dataset()
        augmenter = DataAugmenter(steps=[ResampleStep()])

        for role in [DatasetRole.TRAIN, DatasetRole.VAL]:
            role_dataset: TraceDataset = splits[role]
            role_dataset.prepare_for_training(augmenter)
            n_expected = self.split_counts[role]

            self.assertEqual(n_expected, len(role_dataset))

            model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
            trainer_dataset = role_dataset.to_hf_dataset(model_generator)
            n_links = len(trainer_dataset)

            self.assertTrue(isinstance(trainer_dataset[0], dict))
            self.assertEqual(n_expected, n_links)

    def get_expected_train_dataset_size(self, validation_percentage=BaseTraceTest.VAlIDATION_PERCENTAGE):
        """
        Calculates the size of the training split.
        :param validation_percentage: The percentage of the dataset used for validation.
        :return: The balanced dataset size for training.
        """
        train_percentage = (1 - validation_percentage)
        n_negative = round(self.N_NEGATIVE * train_percentage)
        return n_negative * 2  # equal number pos and neg links
