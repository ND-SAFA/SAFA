import os

from data.creators.coest_dataset_creator import CoestDatasetCreator
from test.base_test import BaseTest
from test.paths.paths import TEST_DATA_DIR


class TestCoestDatasetCreator(BaseTest):
    project_path = os.path.join(TEST_DATA_DIR, "coest")

    def test_positive_links(self):
        dataset_creator = CoestDatasetCreator(self.project_path)
        dataset = dataset_creator.create()

        self.assertEqual(4, len(dataset.pos_link_ids))
        self.assertEqual(4, len(dataset.neg_link_ids))
