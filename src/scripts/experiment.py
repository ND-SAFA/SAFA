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


def expand_paths(value):
    if isinstance(value, list):
        return [expand_paths(v) for v in value]
    if isinstance(value, dict):
        return {k: expand_paths(v) for k, v in value.items()}
    if isinstance(value, str):
        if "~" in value:
            return os.path.expanduser(value)
    return value


if __name__ == "__main__":
    #
    # IMPORTS
    #
    from experiments.experiment import Experiment
    from util.object_creator import ObjectCreator
    from util.file_util import FileUtil

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='Experiment',
        description='Runs experiment definitions')
    parser.add_argument('file')
    args = parser.parse_args()
    file_path = os.path.expanduser(args.file)
    #
    # Job Data Creation
    #
    job_definition = FileUtil.read_json_file(file_path)
    job_definition = expand_paths(job_definition)
    #
    # Logs
    #
    print("GPUS : ", torch.cuda.device_count())
    #
    # Run Job
    #
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8:"
    torch.use_deterministic_algorithms(True)

    application = get_wsgi_application()
    experiment = ObjectCreator.create(Experiment, override=True, **job_definition)
    experiment.run()
