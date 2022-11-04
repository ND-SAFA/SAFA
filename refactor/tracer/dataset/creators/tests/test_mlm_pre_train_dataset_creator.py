import os

from test.base_test import BaseTest
from test.config.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from tracer.dataset.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.dataset.pre_train_dataset import PreTrainDataset


class TestMLMPreTrainDatasetCreator(BaseTest):
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")
    FILENAMES = ["file1.txt", "file2.txt"]
    DATAFILE = os.path.join(PRETRAIN_DIR, FILENAMES[0])
    EXPECTED_OUTPUT_FILE1 = "south bend is very cold and nothing stays open late and all the cars are broken"
    EXPECTED_OUTPUT_FILE2 = " is south bend actually hawkins we might never know"

    def test_create(self):
        dataset_creator = self.get_mlm_pre_train_dataset_creator()
        dataset = dataset_creator.create()
        self.assertTrue(isinstance(dataset, PreTrainDataset))
        with open(dataset_creator.training_dataset_file) as data_file:
            output_lines = data_file.readlines()
        output = " ".join([line.removesuffix("\n") for line in output_lines])
        self.assertEquals(self.EXPECTED_OUTPUT_FILE1+self.EXPECTED_OUTPUT_FILE2, output)

    def test_get_file_list(self):
        files_dir = MLMPreTrainDatasetCreator._get_file_list(self.PRETRAIN_DIR)
        self.assert_lists_have_the_same_vals(self.FILENAMES, files_dir)
        files_single = MLMPreTrainDatasetCreator._get_file_list(self.DATAFILE)
        self.assert_lists_have_the_same_vals([self.FILENAMES[0]], files_single)

    def test_read_data_files(self):
        dataset_creator = self.get_mlm_pre_train_dataset_creator()
        training_examples = dataset_creator._read_data_files(
            [os.path.join(self.PRETRAIN_DIR, filename) for filename in self.FILENAMES])
        result = " ".join(training_examples)
        self.assertEqual(self.EXPECTED_OUTPUT_FILE1 + self.EXPECTED_OUTPUT_FILE2, result)

    def test_read_data_file(self):
        dataset_creator = self.get_mlm_pre_train_dataset_creator()
        training_examples = dataset_creator._read_data_file(self.DATAFILE)
        result = " ".join(training_examples)
        self.assertEqual(self.EXPECTED_OUTPUT_FILE1, result)

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
                                         pre_processing_params=self.PRE_PROCESSING_PARAMS)
