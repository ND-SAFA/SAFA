import os

from jobs.predict_job import PredictJob
from test.base_test import BaseTest
from test.definition_creator import DefinitionCreator
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR


class TestDefinitionCreator(BaseTest):
    def test_trainer_dataset_manager(self):
        definition = {
            "job_args": {
                "output_dir": TEST_OUTPUT_DIR
            },
            "model_manager": {
                "model_path": "roberta-base"
            },
            "trainer_dataset_manager": {
                "train_dataset_creator": {
                    "objectType": "Safa",
                    "project_path": os.path.join(TEST_DATA_DIR, "safa")
                }
            },
            "trainer_args": {
                "output_dir": TEST_OUTPUT_DIR
            }
        }
        predict_job = DefinitionCreator.create(PredictJob, definition)
        print(predict_job)
        predict_job.run()
