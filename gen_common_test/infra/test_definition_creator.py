import os
from copy import deepcopy

from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.infra.experiment.object_creator import ObjectCreator
from gen_common.infra.experiment.variables.typed_definition_variable import TypedDefinitionVariable
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_DATA_DIR, TEST_OUTPUT_DIR


class TestDefinitionCreator(BaseTest):
    JOB_ARGS_DEFINITION = {
        "output_dir": TEST_OUTPUT_DIR
    }
    MODEL_MANAGER_DEFINITION = {
        "model_path": "roberta-base"
    }
    DATASET_CREATOR_DEFINITION = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
        "project_reader": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "STRUCTURE",
            "project_path": os.path.join(TEST_DATA_DIR, "structure")
        }
    }
    DATASET_MANAGER_DEFINITION = {
        "eval_dataset_creator": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
            **DATASET_CREATOR_DEFINITION
        }
    }
    TRAINER_ARGS_DEFINITION = {"output_dir": TEST_OUTPUT_DIR}
    DEFINITION = {
        "task": "PREDICT",
        "job_args": JOB_ARGS_DEFINITION,
        "model_manager": MODEL_MANAGER_DEFINITION,
        "trainer_dataset_manager": DATASET_MANAGER_DEFINITION,
        "trainer_args": TRAINER_ARGS_DEFINITION
    }

    def test_trainer_creation(self):
        definition = {
            "train_dataset_creator": deepcopy(self.DATASET_CREATOR_DEFINITION)
        }
        trainer_dataset_manager = ObjectCreator.create(TrainerDatasetManager, override=True, **definition)
        self.verify_trainer_dataset_manager(trainer_dataset_manager)

    def verify_trainer_dataset_manager(self, trainer_dataset_manager: TrainerDatasetManager,
                                       target_role: DatasetRole = DatasetRole.TRAIN):
        roles = [e for e in DatasetRole]
        roles.remove(target_role)
        for dataset_role in roles:
            self.assertIsNone(trainer_dataset_manager[dataset_role])
        dataset = trainer_dataset_manager[target_role]

        self.assertEqual(len(dataset._pos_link_ids), 4)
        self.assertEqual(len(dataset._neg_link_ids), 4)
        self.assertEqual(len(dataset.trace_df), 8)
