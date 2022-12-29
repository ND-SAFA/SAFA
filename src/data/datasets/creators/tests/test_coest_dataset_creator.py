import os

from data.datasets.creators.structure_dataset_creator import StructureDatasetCreator
from testres.base_test import BaseTest
from testres.paths.paths import TEST_DATA_DIR


class TestStructureDatasetCreator(BaseTest):
    project_path = os.path.join(TEST_DATA_DIR, "structure")

    def test_create(self):
        dataset_creator = StructureDatasetCreator(self.project_path)
        dataset = dataset_creator.create()

        self.assertEqual(4, len(dataset.pos_link_ids))
        self.assertEqual(4, len(dataset.neg_link_ids))
