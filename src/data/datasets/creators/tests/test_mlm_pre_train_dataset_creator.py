import os

from data.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.datasets.pre_train_dataset import PreTrainDataset
from test.base_test import BaseTest
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from test.test_assertions import TestAssertions
from util.file_util import FileUtil


class TestMLMPreTrainDatasetCreator(BaseTest):
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")
    FILENAMES = ["file1.txt", "file2.txt"]
    DATAFILE = os.path.join(PRETRAIN_DIR, FILENAMES[0])
    FILE1_LINES = ["south bend is very cold",
                   "and nothing stays open late",
                   "and all the cars are broken"]
    FILE2_LINES = ["is south bend actually hawkins", "we might never know"]
    EXPECTED_OUTPUT_FILE1 = " ".join(FILE1_LINES)
    EXPECTED_OUTPUT_FILE2 = " ".join(FILE2_LINES)

    def test_create(self):
        """
        Tests that creating a pre-training data results in the aggregation of files in pre-training directory.
        """
        dataset_creator = self.get_mlm_pre_train_dataset_creator()
        dataset = dataset_creator.create()
        self.assertTrue(isinstance(dataset, PreTrainDataset), "create results in PreTrainDataset")
        training_content = FileUtil.read_file(dataset.training_file_path).split("\n")
        expected_lines = self.FILE1_LINES + self.FILE2_LINES
        TestAssertions.assert_lists_have_the_same_vals(self, training_content, expected_lines)

    def test_write_training_examples(self):
        dataset_creator = self.get_mlm_pre_train_dataset_creator()
        expected_word_list = self.EXPECTED_OUTPUT_FILE1.split()
        output_filepath = dataset_creator._write_training_examples(expected_word_list)
        with open(output_filepath) as data_file:
            output = data_file.readlines()
        expected_output = [line + MLMPreTrainDatasetCreator.DELIMINATOR if i != len(expected_word_list) - 1 else line
                           for i, line in enumerate(expected_word_list)]
        self.assertEqual(expected_output, output)

    def get_mlm_pre_train_dataset_creator(self):
        return MLMPreTrainDatasetCreator(self.PRETRAIN_DIR,
                                         TEST_OUTPUT_DIR,
                                         data_cleaner=self.DATA_CLEANER)
