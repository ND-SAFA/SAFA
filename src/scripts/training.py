import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

if __name__ == "__main__":
    #
    # IMPORTS
    #
    from scripts.base_script import BaseScript
    from jobs.train_job import TrainJob
    from server.serializers.job_factory.training_request_serializer import TrainingRequestSerializer

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='PreTrainer',
        description='Pre-trains a bert model on a directory of documents.')
    parser.add_argument('data')  # positional argument
    parser.add_argument('output')
    parser.add_argument('-model', help="The model to fine-tune.", default="roberta-base")
    parser.add_argument('-epochs', default=20, type=int)
    parser.add_argument('-split', default=0.2, type=float)

    args = parser.parse_args()

    #
    # Create Job Data
    #
    job_definition = {
        "modelPath": args.model,
        "outputDir": args.output,
        "saveJobOutput": True,
        "data": {
            "creator": "SAFA",
            "params": {
                "project_path": args.data
            },
        },
        "val_data": {
            "creator": "SPLIT",
            "params": {
                "val_percentage": args.split
            }
        },
        "augmentationSteps": [
            {
                "creator": "RESAMPLE",
                "params": {
                    "resample_rate": 1
                }
            }
        ],
        "params": {
            "trace_args_params": {
                "num_train_epochs": args.epochs,
                "metrics": ["map", "threshold", "precision", "recall", "confusion_matrix"]
            }
        }
    }
    os.makedirs(job_definition["outputDir"], exist_ok=True)
    base_script = BaseScript(TrainingRequestSerializer, TrainJob)
    base_script.run(job_definition, path_vars=[["data", "params", "project_path"], "outputDir"])
