import os
import sys

from dotenv import load_dotenv

from jobs.train_job import TrainJob
from util.object_creator import ObjectCreator

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

if __name__ == "__main__":
    job_definition = {
        "job_args": {
            "random_seed": "165"
        },
        "model_manager": {
            "model_path": "bert-base-uncased"
        },
        "trainer_args": {
            "output_dir": "~/tgen/test/output",
            "num_train_epochs": 10,
            "per_device_train_batch_size": 4,
            "metrics": [
                "map"
            ]
        },
        "trainer_dataset_manager": {
            "train_dataset_creator": {
                "object_type": "STRUCTURE",
                "project_path": "~/tgen/src/testres/data/structure"
            },
            "val_dataset_creator": {
                "object_type": "SPLIT",
                "val_percentage": 0.8
            }
        }
    }

    train_job = ObjectCreator.create(TrainJob, override=True, **job_definition)
    train_job.run()
