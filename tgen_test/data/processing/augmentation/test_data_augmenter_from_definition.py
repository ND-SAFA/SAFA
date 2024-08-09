from tgen.data.processing.augmentation.data_augmenter import DataAugmenter
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.object_creator import ObjectCreator
from tgen.variables.experimental_variable import ExperimentalVariable


class TestDataAugmenterFromDefinition(BaseTest):
    def test_basic(self):
        definition = {
            "steps": []
        }
        data_augmenter = ObjectCreator.create(DataAugmenter, override=True, **definition)
        self.assertEqual(len(data_augmenter.steps), 0)

    def test_one_step(self):
        definition = {
            "steps": [
                {
                    "object_type": "SOURCE_TARGET_SWAP"
                }
            ]
        }
        data_augmenter = ObjectCreator.create(DataAugmenter, override=True, **definition)
        self.assertEqual(len(data_augmenter.steps), 1)

    def test_experiment(self):
        data_augmenters: ExperimentalVariable = ObjectCreator.create(DataAugmenter)
        n_a = len(data_augmenters[0].steps)
        n_b = len(data_augmenters[1].steps)
        self.assertEqual(n_a, 0)
        self.assertEqual(n_b, 1)
