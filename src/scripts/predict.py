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
    from tracer.models.base_models.supported_base_model import SupportedBaseModel
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
    parser.add_argument('output')
    parser.add_argument('-model', help="The model to pre-train", default="roberta-base")
    args = parser.parse_args()

    #
    # Create Job Data
    #
    job_definition = {
        "baseModel": SupportedBaseModel.AUTO_MODEL,
        "modelPath": args.model,
        "outputDir": args.output,
        "saveJobOutput": True,
        "data": {
            "creator": "CSV",
            "params": {
                "data_file_path": args.data
            },
            "preProcessingSteps": []
        },
        "settings": {
            "trace_args_params": {
                "metrics": ["map_at_k"]
            }
        }
    }
    base_script = BaseScript(args, PredictionRequestSerializer, PredictJob)
    base_script.run(job_definition)
