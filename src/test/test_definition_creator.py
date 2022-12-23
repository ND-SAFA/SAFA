import os

from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from test.base_test import BaseTest
from test.definition_creator import DefinitionCreator
from test.paths.paths import TEST_DATA_DIR


class TestDefinitionCreator(BaseTest):
    def test_trainer_dataset_manager(self):
        definition = {
            "train_dataset_creator": {
                "objectType": "Safa",
                "project_path": os.path.join(TEST_DATA_DIR, "safa")
            }
        }
        trainer_dataset_manager = DefinitionCreator.create(TrainerDatasetManager, definition)
        print(trainer_dataset_manager)
