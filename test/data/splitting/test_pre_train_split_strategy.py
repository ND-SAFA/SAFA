import os
from collections import OrderedDict

from tgen.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tgen.data.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.readers.pre_train_project_reader import PreTrainProjectReader
from tgen.data.splitting.dataset_splitter import DatasetSplitter
from tgen.data.splitting.pre_train_split_strategy import PreTrainSplitStrategy
from test.testres.base_trace_test import BaseTraceTest
from test.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.util.file_util import FileUtil


class TestPreTrainSplitStrategy(BaseTraceTest):
    VAlIDATION_PERCENTAGE = 0.4

    def test_with_splitter(self):
        orig_dataset = self.get_dataset()
        splitter = DatasetSplitter(orig_dataset, OrderedDict({DatasetRole.TRAIN: 1-self.VAlIDATION_PERCENTAGE,
                                                              DatasetRole.VAL: self.VAlIDATION_PERCENTAGE}))
        splits = splitter.split_dataset()
        file_contents = []
        n_lines = 0
        for dataset_role, dataset in splits.items():
            self.assertTrue(os.path.exists(dataset.training_file_path))
            file_content = self.get_file_contents(dataset.training_file_path)
            file_contents.append(file_content)
            n_lines += len(file_content)
        orig_contents = self.get_file_contents(orig_dataset.training_file_path)
        self.assertEquals(n_lines, len(orig_contents))
        self.assertEquals(0, len(set(file_contents[0]).intersection(set(file_contents[1]))))

    def test_create_split(self):
        strategy = self.get_pre_train_split_strategy()
        orig_dataset = self.get_dataset()
        train_dataset, test_dataset = strategy.create_split(orig_dataset, self.VAlIDATION_PERCENTAGE)
        self.assertTrue(os.path.exists(train_dataset.training_file_path))
        orig_contents = self.get_file_contents(orig_dataset.training_file_path)
        train_contents = self.get_file_contents(train_dataset.training_file_path)
        expected_size = len(orig_contents) * (1 - self.VAlIDATION_PERCENTAGE)
        self.assertLessEqual(expected_size - len(train_contents), 1)

    def get_file_contents(self, file_path):
        return FileUtil.read_file(file_path).split(PreTrainProjectReader.DELIMINATOR)

    def get_dataset(self):
        return MLMPreTrainDatasetCreator(orig_data_path=TestMLMPreTrainDatasetCreator.PRETRAIN_DIR,
                                         training_data_dir=TEST_OUTPUT_DIR).create()

    def get_pre_train_split_strategy(self):
        return PreTrainSplitStrategy()
