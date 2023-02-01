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
    from util.file_util import FileUtil
    from data.results.experiment_definition import ExperimentDefinition
    from data.results.experiment_reader import ExperimentReader
    from train.trainer_tools.trace_accelerator import TraceAccelerator
    from util.logging.logger_manager import logger

    #
    # Argument Parsing
    #
    parser = argparse.ArgumentParser(
        prog='Experiment',
        description='Runs experiment definitions')
    parser.add_argument('file')
    args = parser.parse_args()
    file_path = os.path.join(RQ_PATH, args.file)
    job_definition = ExperimentDefinition.read_experiment_definition(file_path)
    #
    #
    #
    experiment_base_path = os.path.dirname(job_definition["output_dir"])
    if TraceAccelerator.is_main_process:
        FileUtil.delete_dir(experiment_base_path)
    TraceAccelerator.wait_for_everyone()
    #
    # Logs
    #
    logger.info("GPUS : ", torch.cuda.device_count())
    #
    # Run Job
    #
    application = get_wsgi_application()
    experiment = ObjectCreator.create(Experiment, override=True, **job_definition)
    experiment.run()
    logger.info("\nExperiment Finished!")
    OUTPUT_DIR = job_definition["output_dir"]
    result_reader = ExperimentReader(OUTPUT_DIR)
    result_reader.print_val()
    result_reader.print_eval()
    sys.exit()
