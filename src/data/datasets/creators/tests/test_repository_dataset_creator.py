import os

from data.datasets.creators.repository_dataset_creator import RepositoryDatasetCreator
from data.datasets.formats.repository_format import RepositoryFormat
from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_DATA_DIR
from test.test_assertions import TestAssertions
from test.test_data_manager import TestDataManager


class TestRepositoryDatasetCreator(BaseTraceTest):
    TRACE_FILES_2_ARTIFACTS = {"commit2issue.csv": ("commit.csv", "issue.csv")}
    KEYS = RepositoryFormat(trace_files_2_artifacts=TRACE_FILES_2_ARTIFACTS)
    REPO_DIR = os.path.join(TEST_DATA_DIR, "repo")
    REPO_DIRNAMES = ["one", "two"]

    def test_create(self):
        dataset_creator = self.get_repo_dataset_creator()
        dataset = dataset_creator.create()
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.pos_link_ids,
                                                       TestDataManager.get_positive_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.links, TestDataManager.get_all_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.neg_link_ids,
                                                       TestDataManager.get_negative_link_ids())

    def get_repo_dataset_creator(self):
        return RepositoryDatasetCreator([os.path.join(self.REPO_DIR, dirname) for dirname in self.REPO_DIRNAMES],
                                        data_cleaner=self.DATA_CLEANER, data_keys=self.KEYS)
