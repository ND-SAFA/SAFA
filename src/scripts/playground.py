import os

from jobs.train_job import TrainJob
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from test.test_object_creator import TestObjectCreator

if __name__ == "__main__":
    job_definition = {
        "job_args": {
            "output_dir": TEST_OUTPUT_DIR,
            "random_seed": 420
        },
        "model_manager": {
            "model_path": "roberta-base"
        },
        "trainer_dataset_manager": {
            "train_dataset_creator": {
                "object_type": "STRUCTURE",
                "project_path": os.path.join(TEST_DATA_DIR, "structure")
            }
        },
        "trainer_args": {
            "output_dir": TEST_OUTPUT_DIR,
            "num_train_epochs": 1
        }
    }
    train_job = TestObjectCreator.create(TrainJob, override=True, **job_definition)
    train_job.run()
