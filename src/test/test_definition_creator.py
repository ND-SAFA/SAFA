import os

from data.datasets.dataset_role import DatasetRole
from jobs.predict_job import PredictJob
from test.base_test import BaseTest
from test.definition_creator import DefinitionCreator
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR


class TestDefinitionCreator(BaseTest):
    DEFINITION = {
        "job_args": {
            "output_dir": TEST_OUTPUT_DIR
        },
        "model_manager": {
            "model_path": "roberta-base"
        },
        "trainer_dataset_manager": {
            "eval_dataset_creator": {
                "objectType": "STRUCTURE",
                "project_path": os.path.join(TEST_DATA_DIR, "coest")
            }
        },
        "trainer_args": {
            "output_dir": TEST_OUTPUT_DIR
        }
    }

    def test_trainer_dataset_manager(self):
        definition = self.DEFINITION.copy()
        predict_job: PredictJob = DefinitionCreator.create(PredictJob, definition)

        # Verify trainer dataset manager
        for dataset_role in [DatasetRole.VAL, DatasetRole.TRAIN]:
            self.assertIsNone(predict_job.trainer_dataset_manager[dataset_role])
        eval_dataset = predict_job.trainer_dataset_manager[DatasetRole.EVAL]

        self.assertEquals(len(eval_dataset.pos_link_ids), 4)
        self.assertEquals(len(eval_dataset.neg_link_ids), 4)
        self.assertEquals(len(eval_dataset.links), 8)

        # Verify trainer args
        definition.pop("trainer_dataset_manager")
        for parent_key, parent_value in definition.items():
            parent_object = getattr(predict_job, parent_key)
            for child_key, child_value in parent_value.items():
                self.assertEquals(getattr(parent_object, child_key), child_value)
