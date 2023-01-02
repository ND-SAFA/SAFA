from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.processing.augmentation.data_augmenter import DataAugmenter
from testres.base_test import BaseTest
from util.object_creator import ObjectCreator
from variables.experimental_variable import ExperimentalVariable


class TestDataAugmenterFromDefinition(BaseTest):
    def test_basic(self):
        definition = {
            "steps": []
        }
        data_augmenter = ObjectCreator.create(DataAugmenter, override=True, **definition)
        self.assertEquals(len(data_augmenter.steps), 0)

    def test_one_step(self):
        definition = {
            "steps": [
                {
                    "object_type": "SOURCE_TARGET_SWAP"
                }
            ]
        }
        data_augmenter = ObjectCreator.create(DataAugmenter, override=True, **definition)
        self.assertEquals(len(data_augmenter.steps), 1)

    def test_experiment(self):
        data_augmenters: ExperimentalVariable = ObjectCreator.create(DataAugmenter)
        n_a = len(data_augmenters[0].value.steps)
        n_b = len(data_augmenters[1].value.steps)
        self.assertEquals(n_a, 0)
        self.assertEquals(n_b, 1)
