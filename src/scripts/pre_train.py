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
    from models.base_models.supported_base_model import SupportedBaseModel
    from jobs.mlm_pre_train_job import MLMPreTrainJob
    from server.serializers.job_factory.pre_training_request_serializer import PreTrainingRequestSerializer

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='PreTrainer',
        description='Pre-trains a bert model on a directory of documents.')
    parser.add_argument('data')
    parser.add_argument('output')
    parser.add_argument('-model', default='robert-base')
    args = parser.parse_args()
    #
    # Job Data Creation
    #
    job_definition = {
        "baseModel": SupportedBaseModel.BERT_FOR_MASKED_LM,
        "modelPath": "roberta-base",
        "trainingDataDir": args.data,
        "outputDir": args.output,
        "saveJobOutput": True
    }
    #
    # Run Job
    #
    base_script = BaseScript(args, PreTrainingRequestSerializer, MLMPreTrainJob)
    base_script.run(job_definition)
