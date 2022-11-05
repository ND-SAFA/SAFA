import os

from test.base_trace_test import BaseTraceTest
from test.config.paths import TEST_DATA_DIR
from tracer.dataset.creators.repository_dataset_creator import RepositoryKeys, RepositoryDatasetCreator


class TestRepositoryDatasetCreator(BaseTraceTest):
    TRACE_FILES_2_ARTIFACTS = {"commit2issue.csv": ("commit.csv", "issue.csv")}
    KEYS = RepositoryKeys(trace_files_2_artifacts=TRACE_FILES_2_ARTIFACTS)
    REPO_DIR = os.path.join(TEST_DATA_DIR, "repo")
    REPO_DIRNAMES = ["one", "two"]

    def test_create(self):
        dataset_creator = self.get_repo_dataset_creator()
        dataset = dataset_creator.create()
        self.assert_lists_have_the_same_vals(dataset.pos_link_ids, self.get_link_ids(self.POS_LINKS))
        self.assert_lists_have_the_same_vals(dataset.links, self.get_link_ids(self.ALL_TEST_LINKS))
        self.assert_lists_have_the_same_vals(dataset.neg_link_ids, self.get_link_ids(self.NEG_LINKS))

    def get_repo_dataset_creator(self):
        return RepositoryDatasetCreator([os.path.join(self.REPO_DIR, dirname) for dirname in self.REPO_DIRNAMES],
                                        pre_processing_params=self.PRE_PROCESSING_PARAMS, data_keys=self.KEYS)
