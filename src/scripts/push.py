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
    from jobs.push_model_job import PushModelJob
    from server.serializers.job_factory.model_identifier_serializer import ModelIdentifierSerializer

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='PreTrainer',
        description='Pre-trains a bert model on a directory of documents.')
    parser.add_argument('model')  # positional argument
    parser.add_argument('export', help="The model to evaluate.")
    args = parser.parse_args()

    #
    # Create Job Data
    #
    job_definition = {
        "modelPath": args.model,
        "outputDir": args.export,
        "saveJobOutput": False,
    }
    base_script = BaseScript(ModelIdentifierSerializer, PushModelJob)
    base_script.run(job_definition, path_vars=["modelPath"])
