import os
from copy import deepcopy

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.predict_job import PredictJob
from test.base_test import BaseTest
from test.definition_creator import DefinitionCreator
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from test.test_object_creator import TestObjectCreator
from util.variables.typed_definition_variable import TypedDefinitionVariable


class TestDefinitionCreator(BaseTest):
    JOB_ARGS_DEFINITION = {
        "output_dir": TEST_OUTPUT_DIR
    }
    MODEL_MANAGER_DEFINITION = {
        "model_path": "roberta-base"
    }
    DATASET_CREATOR_DEFINITION = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "STRUCTURE",
        "project_path": os.path.join(TEST_DATA_DIR, "structure")
    }
    DATASET_MANAGER_DEFINITION = {
        "eval_dataset_creator": DATASET_CREATOR_DEFINITION
    }
    TRAINER_ARGS_DEFINITION = {"output_dir": TEST_OUTPUT_DIR}
    DEFINITION = {
        "job_args": JOB_ARGS_DEFINITION,
        "model_manager": MODEL_MANAGER_DEFINITION,
        "trainer_dataset_manager": DATASET_MANAGER_DEFINITION,
        "trainer_args": TRAINER_ARGS_DEFINITION
    }

    def test_trainer_creation(self):
        definition = {
            "train_dataset_creator": deepcopy(self.DATASET_CREATOR_DEFINITION)
        }
        trainer_dataset_manager = TestObjectCreator.create(TrainerDatasetManager, override=True, **definition)
        self.verify_trainer_dataset_manager(trainer_dataset_manager)

    def test_trainer_dataset_manager(self):
        definition = deepcopy(self.DEFINITION)
        predict_job: PredictJob = DefinitionCreator.create(PredictJob, definition)

        # Verify trainer dataset manager
        self.verify_trainer_dataset_manager(predict_job.trainer_dataset_manager, DatasetRole.EVAL)

        # Verify trainer args
        definition.pop("trainer_dataset_manager")
        for parent_key, parent_value in definition.items():
            parent_object = getattr(predict_job, parent_key)
            for child_key, child_value in parent_value.items():
                self.assertEquals(getattr(parent_object, child_key), child_value)

    def verify_trainer_dataset_manager(self, trainer_dataset_manager: TrainerDatasetManager,
                                       target_role: DatasetRole = DatasetRole.TRAIN):
        roles = [e for e in DatasetRole]
        roles.remove(target_role)
        for dataset_role in roles:
            self.assertIsNone(trainer_dataset_manager[dataset_role])
        dataset = trainer_dataset_manager[target_role]

        self.assertEquals(len(dataset.pos_link_ids), 4)
        self.assertEquals(len(dataset.neg_link_ids), 4)
        self.assertEquals(len(dataset.links), 8)
