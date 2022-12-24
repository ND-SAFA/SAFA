import os

from data.datasets.creators.safa_dataset_creator import SafaDatasetCreator
from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_DATA_DIR


class TestSafaDatasetCreator(BaseTraceTest):
    TRACE_FILES_2_ARTIFACTS = {"Layer1Source2Target.json": ("Layer1Source.json", "Layer1Target.json"),
                               "Layer2Source2Target.json": ("Layer2Source.json", "Layer2Target.json"),
                               }
    SAFA_DATA_DIR = os.path.join(TEST_DATA_DIR, "safa")

    def test_create(self):
        dataset_creator = self.get_safa_dataset_creator()
        dataset = dataset_creator.create()
        self.assert_lists_have_the_same_vals(dataset.pos_link_ids, self.get_link_ids(self.POS_LINKS))
        self.assert_lists_have_the_same_vals(dataset.links, self.get_link_ids(self.ALL_TEST_LINKS))
        self.assert_lists_have_the_same_vals(dataset.neg_link_ids, self.get_link_ids(self.NEG_LINKS))

    def get_safa_dataset_creator(self):
        return SafaDatasetCreator(self.SAFA_DATA_DIR, data_cleaner=self.DATA_CLEANER)
