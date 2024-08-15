import os
from copy import deepcopy

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from common_resources.data.tdatasets.dataset_role import DatasetRole
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.definition_creator import DefinitionCreator
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from common_resources.tools.variables.typed_definition_variable import TypedDefinitionVariable


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

    def test_trainer_dataset_manager(self):
        definition = deepcopy(self.DEFINITION)
        predict_job: HuggingFaceJob = DefinitionCreator.create(HuggingFaceJob, definition)

        # Verify trainer dataset manager
        self.verify_trainer_dataset_manager(predict_job.trainer_dataset_manager, DatasetRole.EVAL)

        # Verify trainer args
        definition.pop("trainer_dataset_manager")
        for parent_key, parent_value in definition.items():
            parent_object = getattr(predict_job, parent_key)
            if isinstance(parent_value, dict):
                for child_key, child_value in parent_value.items():
                    parent_object_key = getattr(parent_object, child_key)
                    self.assertEqual(parent_object_key, child_value)
            elif isinstance(parent_value, str):
                self.assertIn(parent_value, str(parent_object))

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
