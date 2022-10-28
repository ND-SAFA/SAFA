import os

from test.base_test import BaseTest
from test.config.paths import TEST_DATA_DIR
from tracer.dataset.creators.csv_dataset_creator import CSVDatasetCreator


class TestCSVDatasetCreator(BaseTest):
    TEST_DATA_FILE = "test_csv_data.csv"
    CSV_DATA_DIR = os.path.join(TEST_DATA_DIR, "csv")

    def test_create(self):
        dataset_creator = self.get_csv_dataset_creator()
        dataset = dataset_creator.create()
        self.assert_lists_have_the_same_vals(dataset.pos_link_ids, self.get_link_ids(self.POS_LINKS))
        self.assert_lists_have_the_same_vals(dataset.links, self.get_link_ids(self.ALL_TEST_LINKS))
        self.assert_lists_have_the_same_vals(dataset.neg_link_ids, self.get_link_ids(self.NEG_LINKS))

    def get_csv_dataset_creator(self):
        data_file_path = os.path.join(self.CSV_DATA_DIR, self.TEST_DATA_FILE)
        return CSVDatasetCreator(data_file_path, self.PRE_PROCESSING_PARAMS)
