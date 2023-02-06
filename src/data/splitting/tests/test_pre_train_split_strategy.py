from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from data.splitting.dataset_splitter import DatasetSplitter
from data.splitting.pre_train_split_strategy import PreTrainSplitStrategy
from testres.base_trace_test import BaseTraceTest
from testres.paths.paths import TEST_OUTPUT_DIR


class TestPreTrainSplitStrategy(BaseTraceTest):

    def test_one(self):
        strategy = self.get_pre_train_split_strategy()
        splitter = DatasetSplitter(self.get_dataset())
        train_dataset, test_dataset = splitter.split(0.6)
        # TODO

    def get_dataset(self):
        return MLMPreTrainDatasetCreator(orig_data_path=TestMLMPreTrainDatasetCreator.PRETRAIN_DIR,
                                         training_data_dir=TEST_OUTPUT_DIR).create()

    def get_pre_train_split_strategy(self):
        return PreTrainSplitStrategy()
