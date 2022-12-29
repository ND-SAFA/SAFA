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
    from experiments.experiment import Experiment
    from test.test_object_creator import TestObjectCreator
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
    #
    # Run Job
    #
    experiment = TestObjectCreator.create(Experiment, override=True, **job_definition)
    experiment.run()
