import argparse
import os
import sys

import torch
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])
if __name__ == "__main__":
    #
    # IMPORTS
    #
    from experiments.experiment import Experiment
    from util.object_creator import ObjectCreator
    from scripts.script_utils import read_job_definition
    from util.file_util import FileUtil

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='Experiment',
        description='Runs experiment definitions')
    parser.add_argument('file')
    args = parser.parse_args()
    file_path = os.path.join(RQ_PATH, args.file)
    job_definition = read_job_definition(file_path)
    #
    #
    #
    experiment_base_path = os.path.dirname(job_definition["output_dir"])
    FileUtil.delete_dir(experiment_base_path)
    #
    # Logs
    #
    print("GPUS : ", torch.cuda.device_count())
    #
    # Run Job
    #
    application = get_wsgi_application()
    experiment = ObjectCreator.create(Experiment, override=True, **job_definition)
    experiment.run()
    print("\nFinished. Have a good day :)")
