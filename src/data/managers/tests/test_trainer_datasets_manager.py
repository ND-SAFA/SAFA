import os
from typing import List
from unittest.mock import patch

from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.datasets.dataset_role import DatasetRole
from data.datasets.trace_dataset import TraceDataset
from data.managers.tests.base_trainer_datasets_manager_test import BaseTrainerDatasetsManagerTest
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from testres.paths.paths import TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
from util.object_creator import ObjectCreator
from variables.experimental_variable import ExperimentalVariable


class TestTrainerDatasetsManager(BaseTrainerDatasetsManagerTest):
    @patch.object(MLMPreTrainDatasetCreator, "create")
    def test_prepare_datasets(self, create_mock):
        dataset_container_manager: TrainerDatasetManager = self.create_dataset_manager(
            [DatasetRole.PRE_TRAIN, DatasetRole.EVAL, DatasetRole.VAL])
        dataset_container_manager._prepare_datasets([])
        self.assert_final_datasets_are_as_expected(dataset_container_manager)

    @patch.object(MLMPreTrainDatasetCreator, "create")
    def test_create_dataset_splits(self, create_mock):
        dataset_container_manager = self.create_dataset_manager([DatasetRole.VAL, DatasetRole.EVAL])
        expected_dataset_split_roles = [DatasetRole.TRAIN, DatasetRole.VAL, DatasetRole.EVAL]
        train_dataset = dataset_container_manager[DatasetRole.TRAIN]
        splits = TrainerDatasetManager._create_dataset_splits(train_dataset,
                                                              dataset_container_manager._dataset_creators)

        for dataset_role in expected_dataset_split_roles:
            self.assertIn(dataset_role, splits)
            self.assertTrue(isinstance(splits[dataset_role], TraceDataset))
        self.assertNotIn(DatasetRole.PRE_TRAIN, splits)

    def test_get_creator(self):
        dataset_container_manager = self.create_dataset_manager(
            [DatasetRole.PRE_TRAIN, DatasetRole.VAL, DatasetRole.EVAL])
        self.assertIsInstance(dataset_container_manager.get_creator(DatasetRole.TRAIN), TraceDatasetCreator)

    def test_save_dataset_splits(self):
        if not os.path.exists(TEST_OUTPUT_DIR):
            os.makedirs(TEST_OUTPUT_DIR)
        dataset_container_manager = self.create_dataset_manager([DatasetRole.VAL])
        dataset_container_manager.save_dataset_splits(TEST_OUTPUT_DIR)
        TestAssertions.assert_lists_have_the_same_vals(self, ["train.csv", "val.csv"], os.listdir(TEST_OUTPUT_DIR))

    @patch.object(MLMPreTrainDatasetCreator, "create")
    def test_create_from_map(self, create_mock):
        dataset_container_manager = self.create_dataset_manager(
            [DatasetRole.PRE_TRAIN, DatasetRole.VAL])
        self.assertTrue(dataset_container_manager[DatasetRole.PRE_TRAIN] is not None)
        self.assertIsInstance(dataset_container_manager[DatasetRole.TRAIN], TraceDataset)

    def _create_datasets_from_creators(self):
        dataset_container_manager = self.create_dataset_manager(
            [DatasetRole.PRE_TRAIN, DatasetRole.VAL, DatasetRole.EVAL])
        self.assert_final_datasets_are_as_expected(dataset_container_manager)

    def test_get_set_bad_index(self):
        dataset_container_manager = self.create_dataset_manager(
            [DatasetRole.VAL, DatasetRole.EVAL])
        try:
            dataset_container_manager[DatasetRole.EVAL] = None
            self.fail("Did not raise Exception on bad index")
        except Exception:
            pass

    def create_dataset_manager(self, keys: List[DatasetRole], experiment: bool = False) -> TrainerDatasetManager:
        dataset_creators = {
            DatasetRole.PRE_TRAIN: ("pre_train_dataset_creator", ObjectCreator.pretrain_dataset_definition),
            DatasetRole.EVAL: ("eval_dataset_creator", self.eval_dataset_creator_definition),
            DatasetRole.VAL: ("val_dataset_creator", self.val_dataset_creator_definition)
        }
        args = {}
        for key in keys:
            arg_name, definition = dataset_creators[key]
            args[arg_name] = definition
        args["augmenter"] = ObjectCreator.augmenter_definition
        managers: ExperimentalVariable = ObjectCreator.create(TrainerDatasetManager, **args)
        if not experiment:
            managers = managers.get_values_of_all_variables()[-1]
        return managers
