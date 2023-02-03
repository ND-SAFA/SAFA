import argparse
import os
import sys

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
    from util.logging.logger_manager import LoggerManager, logger
    from util.logging.logger_config import LoggerConfig

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
    job_output_dir = job_definition["output_dir"]
    LoggerManager.configure_logger(LoggerConfig(output_dir=job_output_dir))
    #
    #
    #
    experiment_base_path = os.path.dirname(job_definition["output_dir"])
    if TraceAccelerator.is_main_process:
        FileUtil.delete_dir(experiment_base_path)
    TraceAccelerator.wait_for_everyone()
    #
    # Run Job
    #
    application = get_wsgi_application()
    experiment = ObjectCreator.create(Experiment, override=True, **job_definition)
    # LoggerManager.turn_off_hugging_face_logging()
    experiment.run()
    logger.info("\nExperiment Finished!")

    result_reader = ExperimentReader(job_output_dir)
    result_reader.print_val()
    result_reader.print_eval()
    sys.exit()
