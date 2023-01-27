import os

from data.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from testres.base_test import BaseTest
from testres.paths.paths import TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
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

    def test_move_dir_contents(self):
        """
        Tests that move dir contents moves all files inside the directory to the specified location
        """
        orig_dir = os.path.join(TEST_OUTPUT_DIR, "orig_dir")
        files = ["file1.txt", "file2.txt"]
        for filename in files:  # create empty files
            FileUtil.safe_open_w(os.path.join(orig_dir, filename))
        new_dir = os.path.join(TEST_OUTPUT_DIR, "new_dir")
        FileUtil.move_dir_contents(orig_dir, new_dir, delete_after_move=True)
        for filename in files:  # create empty files
            self.assertTrue(os.path.exists(os.path.join(new_dir, filename)))
        self.assertFalse(os.path.exists(os.path.join(TEST_OUTPUT_DIR, orig_dir)))
