import os
from typing import List

from data.datasets.dataset_role import DatasetRole
from data.managers.deterministic_trainer_dataset_manager import DeterministicTrainerDatasetManager
from data.managers.tests.base_trainer_datasets_manager_test import BaseTrainerDatasetsManagerTest
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator
from variables.experimental_variable import ExperimentalVariable


class TestDeterministicTrainerDatasetsManager(BaseTrainerDatasetsManagerTest):
    DETERMINISTIC_ID = "deterministic"
    OUTPUT_DIR = os.path.join(TEST_OUTPUT_DIR, DETERMINISTIC_ID)

    def test_get_datasets(self):
        expected_dataset_roles = [DatasetRole.TRAIN, DatasetRole.VAL, DatasetRole.EVAL]
        dataset_container_manager_first = self.create_dataset_manager(expected_dataset_roles[1:])
        datasets1 = dataset_container_manager_first.get_datasets()
        self.assert_final_datasets_are_as_expected(dataset_container_manager_first, include_pretrain=False)
        self.assertTrue(os.path.exists(dataset_container_manager_first.get_output_path()))
        dataset_files = os.listdir(dataset_container_manager_first.get_output_path())
        for dataset_role in expected_dataset_roles:
            self.assertIn(dataset_container_manager_first._get_dataset_filename(dataset_role,
                                                                                dataset_container_manager_first.dataset_name),
                          dataset_files)
        dataset_container_manager_second = self.create_dataset_manager(expected_dataset_roles[1:])
        datasets2 = dataset_container_manager_second.get_datasets()
        for dataset_role, dataset in datasets1.items():
            if dataset_role in expected_dataset_roles[1:]:
                self.assertListEqual(sorted(dataset.pos_link_ids), sorted(datasets2[dataset_role].pos_link_ids))

    def create_dataset_manager(self, keys: List[DatasetRole]):
        args = ObjectCreator.get_definition(TrainerDatasetManager)
        dataset_creators = {
            DatasetRole.EVAL: ("eval_dataset_creator", self.eval_dataset_creator_definition),
            DatasetRole.VAL: ("val_dataset_creator", self.val_dataset_creator_definition)
        }
        for key in keys:
            arg_name, definition = dataset_creators[key]
            args[arg_name] = definition
        args["augmenter"] = ObjectCreator.augmenter_definition
        args["random_seed"] = 10
        args["output_dir"] = TEST_OUTPUT_DIR
        experiment_vars: ExperimentalVariable = ObjectCreator.create(DeterministicTrainerDatasetManager, override=True, **args)
        return experiment_vars.get_values_of_all_variables()[-1]
