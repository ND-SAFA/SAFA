import os

from data.datasets.creators.safa_dataset_creator import SafaDatasetCreator
from testres.base_trace_test import BaseTraceTest
from testres.paths.paths import TEST_DATA_DIR
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager


class TestSafaDatasetCreator(BaseTraceTest):
    TRACE_FILES_2_ARTIFACTS = {"Layer1Source2Target.json": ("Layer1Source.json", "Layer1Target.json"),
                               "Layer2Source2Target.json": ("Layer2Source.json", "Layer2Target.json"),
                               }
    SAFA_DATA_DIR = os.path.join(TEST_DATA_DIR, "safa")

    def test_create(self):
        dataset_creator = self.get_safa_dataset_creator()
        dataset = dataset_creator.create()
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.pos_link_ids,
                                                       TestDataManager.get_positive_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.links, TestDataManager.get_all_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.neg_link_ids,
                                                       TestDataManager.get_negative_link_ids())

    def get_safa_dataset_creator(self):
        return SafaDatasetCreator(self.SAFA_DATA_DIR, data_cleaner=self.DATA_CLEANER)
