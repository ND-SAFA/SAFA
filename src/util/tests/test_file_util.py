import os

from data.datasets.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from test.base_test import BaseTest
from test.test_assertions import TestAssertions
from util.file_util import FileUtil


class TestFileUtil(BaseTest):
    def test_get_file_list(self):
        """
        Tests that pre-training data creator is able to retrieve relevant files in pre-training directory.
        """
        files_dir = FileUtil.get_file_list(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        expected_files = list(map(lambda f: os.path.join(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR, f),
                                  TestMLMPreTrainDatasetCreator.FILENAMES))
        TestAssertions.assert_lists_have_the_same_vals(self, expected_files, files_dir)
        files_single = FileUtil.get_file_list(TestMLMPreTrainDatasetCreator.DATAFILE)
        TestAssertions.assert_lists_have_the_same_vals(self, [expected_files[0]], files_single)
