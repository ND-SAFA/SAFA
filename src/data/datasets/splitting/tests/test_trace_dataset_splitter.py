from unittest import mock
from unittest.mock import patch

from data.datasets.splitting.random_split_strategy import RandomSplitStrategy
from data.datasets.splitting.supported_split_strategy import SupportedSplitStrategy
from data.datasets.splitting.trace_dataset_splitter import TraceDatasetSplitter
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager


class TestTraceDatasetSplitter(BaseTraceTest):

    def test_splits(self):
        for split_type in SupportedSplitStrategy:
            if split_type == SupportedSplitStrategy.RANDOM_ALL_SOURCES:
                self.assert_split(split_type)
                self.assert_split_multiple(split_type)

    def assert_split_multiple(self, strategy=SupportedSplitStrategy.RANDOM):
        trace_dataset = self.get_trace_dataset()
        n_orig_links = len(trace_dataset)
        percent_splits = [0.3, 0.2]
        splitter = TraceDatasetSplitter(trace_dataset)
        splits = splitter.split_multiple(percent_splits, strategies=[strategy.name] * len(percent_splits))
        length_of_splits = [len(split) for split in splits]
        split_link_ids = [set(split.links.keys()) for split in splits]
        self.assertEquals(sum(length_of_splits), n_orig_links)
        for i, len_split in enumerate(length_of_splits):
            if i == 0:
                self.assertLessEqual(abs(len_split - round(n_orig_links * (1 - sum(percent_splits)))), 1)
                continue
            self.assertLessEqual(abs(len_split - round(n_orig_links * percent_splits[i - 1])), 1)
        for i, split in enumerate(splits):
            link_ids = split_link_ids[i]
            for j, other_link_ids in enumerate(split_link_ids):
                if i == j:
                    continue
                intersection = other_link_ids.intersection(link_ids)
                self.assertEquals(len(intersection), 0)

    def assert_split(self, strategy=SupportedSplitStrategy.RANDOM):
        trace_dataset = self.get_trace_dataset()
        splitter = TraceDatasetSplitter(trace_dataset)
        split1, split2 = splitter.split(self.VAlIDATION_PERCENTAGE, strategy=strategy.name)
        expected_val_link_size = (self.EXPECTED_VAL_SIZE_POS_LINKS + self.EXPECTED_VAL_SIZE_NEG_LINKS)
        self.assertLessEqual(abs(len(split1) - (len(self.all_links) - expected_val_link_size)), 1)
        self.assertLessEqual(abs(len(split2) - expected_val_link_size), 1)
        intersection = set(split1.links.keys()).intersection(set(split2.links.keys()))
        self.assertEquals(len(intersection), 0)

        for split in [split1, split2]:
            link_ids = split.pos_link_ids + split.neg_link_ids
            TestAssertions.assert_lists_have_the_same_vals(self, split.links.keys(), link_ids)

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

    def test_get_data_split(self):
        positive_links = list(self.positive_links.values())
        split1 = RandomSplitStrategy.get_data_split(positive_links, self.VAlIDATION_PERCENTAGE, for_second_split=False)
        split2 = RandomSplitStrategy.get_data_split(positive_links, self.VAlIDATION_PERCENTAGE, for_second_split=True)
        self.assertEquals(len(split1), self.N_POSITIVE - self.EXPECTED_VAL_SIZE_POS_LINKS)
        self.assertEquals(len(split2), self.EXPECTED_VAL_SIZE_POS_LINKS)
        intersection = set(split1).intersection(set(split2))
        self.assertEquals(len(intersection), 0)

    def test_get_first_split_size(self):
        size = RandomSplitStrategy.get_first_split_size(TestDataManager.get_positive_links(),
                                                        self.VAlIDATION_PERCENTAGE)
        self.assertEquals(size, self.N_POSITIVE - self.EXPECTED_VAL_SIZE_POS_LINKS)

    def get_expected_train_dataset_size(self, resample_rate=BaseTraceTest.RESAMPLE_RATE,
                                        validation_percentage=BaseTraceTest.VAlIDATION_PERCENTAGE):
        num_train_pos_links = round(self.N_POSITIVE * (1 - validation_percentage))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links
