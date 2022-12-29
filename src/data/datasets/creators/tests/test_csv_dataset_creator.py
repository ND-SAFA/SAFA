import os

from data.datasets.creators.csv_dataset_creator import CSVDatasetCreator
from testres.base_trace_test import BaseTraceTest
from testres.paths.paths import TEST_DATA_DIR
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager


class TestCSVDatasetCreator(BaseTraceTest):
    TEST_DATA_FILE = "test_csv_data.csv"
    CSV_DATA_DIR = os.path.join(TEST_DATA_DIR, "csv")

    def test_create(self):
        dataset_creator = self.get_csv_dataset_creator()
        dataset = dataset_creator.create()
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.pos_link_ids,
                                                       TestDataManager.get_positive_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.links, TestDataManager.get_all_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.neg_link_ids,
                                                       TestDataManager.get_negative_link_ids())

    def get_csv_dataset_creator(self):
        data_file_path = os.path.join(self.CSV_DATA_DIR, self.TEST_DATA_FILE)
        return CSVDatasetCreator(data_file_path, data_cleaner=self.DATA_CLEANER)
