import os

from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_OUTPUT_DIR
from tracer.datasets.trace_dataset import TraceDataset
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class TestTrainerDatasetsContainer(BaseTraceTest):

    def test_save_dataset_splits(self):
        if not os.path.exists(TEST_OUTPUT_DIR):
            os.makedirs(TEST_OUTPUT_DIR)
        datasets_container = self.get_trainer_datasets_container()
        datasets_container.save_dataset_splits(TEST_OUTPUT_DIR)
        self.assert_lists_have_the_same_vals(["train.csv", "val.csv"], os.listdir(TEST_OUTPUT_DIR))

    def get_trace_dataset(self):
        links = self.get_links(self.ALL_TEST_LINKS)
        pos_links_ids = self.get_link_ids(self.POS_LINKS)
        neg_link_ids = self.get_link_ids(self.NEG_LINKS)
        return TraceDataset(links, pos_links_ids, neg_link_ids)

    def get_trainer_datasets_container(self):
        return TrainerDatasetsContainer(train=self.get_trace_dataset(), split_train_dataset=True)
