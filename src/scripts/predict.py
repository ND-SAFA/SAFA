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
    from jobs.predict_job import PredictJob
    from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer
    from scripts.base_script import BaseScript

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='PreTrainer',
        description='Pre-trains a bert model on a directory of documents.')
    parser.add_argument('data')  # positional argument
    parser.add_argument('model', help="The model to evaluate.")
    parser.add_argument('-output', default=None)
    args = parser.parse_args()

    #
    # Create Job Data
    #
    output = args.output if args.output else args.model
    job_definition = {
        "modelPath": args.model,
        "outputDir": output,
        "saveJobOutput": True,
        "data": {
            "creator": "SAFA",
            "params": {
                "project_path": args.data
            },
        },
        "params": {
            "trace_args_params": {
                "metrics": ["map", "threshold", "precision", "recall", "confusion_matrix"]
            }
        }
    }
    base_script = BaseScript(PredictionRequestSerializer, PredictJob)
    base_script.run(job_definition, path_vars=[["data", "params", "project_path"], "modelPath"])
