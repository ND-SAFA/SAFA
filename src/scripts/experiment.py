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

ENV_REPLACEMENT_VARIABLES = ["DATA_PATH", "ROOT_PATH"]


def get_env_replacements():
    replacements = {}
    for replacement_path in ENV_REPLACEMENT_VARIABLES:
        path_value = os.environ.get(replacement_path, None)
        if path_value:
            path_key = "[%s]" % replacement_path
            replacements[path_key] = os.path.expanduser(path_value)
    return replacements


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
    env_replacements = get_env_replacements()
    job_definition = FileUtil.read_json_file(file_path)
    job_definition = FileUtil.expand_paths_in_dictionary(job_definition, env_replacements)
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
