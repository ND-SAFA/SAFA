import os
from typing import List

from tgen.data.managers.deterministic_trainer_dataset_manager import DeterministicTrainerDatasetManager
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.testres.base_tests.base_trainer_datasets_manager_test import BaseTrainerDatasetsManagerTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.variables.experimental_variable import ExperimentalVariable


class TestDeterministicTrainerDatasetsManager(BaseTrainerDatasetsManagerTest):
    DETERMINISTIC_ID = "deterministic"
    OUTPUT_DIR = os.path.join(TEST_OUTPUT_DIR, DETERMINISTIC_ID)

    def test_get_datasets(self):
        expected_dataset_roles = [DatasetRole.TRAIN, DatasetRole.VAL, DatasetRole.EVAL]
        deterministic_dataset_manager = self.create_dataset_manager(expected_dataset_roles[1:])
        role2dataset = deterministic_dataset_manager.get_datasets()
        self.assert_final_datasets_are_as_expected(deterministic_dataset_manager, include_pretrain=False)
        self.assertTrue(os.path.exists(deterministic_dataset_manager.get_output_path()))
        dataset_files = os.listdir(deterministic_dataset_manager.get_output_path())
        for dataset_role in expected_dataset_roles:
            dataset_file_name = deterministic_dataset_manager.get_dataset_filename(dataset_role,
                                                                                   deterministic_dataset_manager.dataset_name)
            self.assertIn(dataset_file_name, dataset_files)
        dataset_container_manager_second = self.create_dataset_manager(expected_dataset_roles[1:])
        datasets2 = dataset_container_manager_second.get_datasets()
        for dataset_role, dataset in role2dataset.items():
            if dataset_role in expected_dataset_roles[1:]:
                self.assertListEqual(sorted(dataset.get_pos_link_ids()), sorted(datasets2[dataset_role].get_pos_link_ids()))

    def create_dataset_manager(self, dataset_roles: List[DatasetRole]):
        args = ObjectCreator.get_definition(TrainerDatasetManager)
        dataset_creators = {
            DatasetRole.EVAL: ("eval_dataset_creator", self.eval_dataset_creator_definition),
            DatasetRole.VAL: ("val_dataset_creator", self.val_dataset_creator_definition)
        }
        for role in dataset_roles:
            arg_name, definition = dataset_creators[role]
            args[arg_name] = definition
        args["augmenter"] = ObjectCreator.augmenter_definition
        args["random_seed"] = 10
        args["output_dir"] = TEST_OUTPUT_DIR
        experiment_vars: ExperimentalVariable = ObjectCreator.create(DeterministicTrainerDatasetManager, override=True, **args)
        return experiment_vars.get_values_of_all_variables()[-1]
