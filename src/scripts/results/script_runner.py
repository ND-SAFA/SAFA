import os
from typing import Dict

from django.core.wsgi import get_wsgi_application

from experiments.experiment import Experiment
from scripts.results.script_definition import ScriptDefinition
from scripts.results.script_reader import ExperimentReader
from train.trainer_tools.trace_accelerator import TraceAccelerator
from util.file_util import FileUtil
from util.logging.logger_config import LoggerConfig
from util.logging.logger_manager import LoggerManager, logger
from util.object_creator import ObjectCreator


class ScriptRunner:
    """
    Responsible for reading/preprocessing script definition, running script, and reading results.
    ---
    Script Definition: JSON file definition experiment definition using any syntactic sugars.
    """
    FINISHED_HEADER = "Experiment Finished! :)"

    def __init__(self, script_definition_path: str):
        """
        Initializes runner for definition at path.
        :param script_definition_path: Path to the script definition defining experiment to open.
        """
        self.script_definition_path = script_definition_path
        self.experiment_definition = None
        self.experiment_dir = None
        self.logging_dir = None

    def run(self) -> None:
        """
        Runs experiment defined by definition
        :return: None
        """
        experiment_definition = self._load_experiment_definition()
        self._setup_run()
        experiment = ObjectCreator.create(Experiment, override=True, **experiment_definition)
        LoggerManager.turn_off_hugging_face_logging()
        experiment.run()
        logger.info(self.FINISHED_HEADER)

    def print_results(self) -> None:
        """
        Prints the results of the experiment.
        :return:
        """
        self._load_experiment_definition()
        result_reader = ExperimentReader(self.experiment_dir)
        result_reader.print_val()
        result_reader.print_eval()

    def _load_experiment_definition(self) -> Dict:
        """
        Reads script definition.
        :return:
        """
        if self.experiment_definition is None:
            self.experiment_definition = ScriptDefinition.read_experiment_definition(self.script_definition_path)
            experiment_definition = self._load_experiment_definition()
            self.experiment_dir = experiment_definition[ScriptDefinition.OUTPUT_DIR_PARAM]
            self.logging_dir = experiment_definition.pop(ScriptDefinition.LOGGING_DIR_PARAM)
            os.makedirs(self.logging_dir, exist_ok=True)
            LoggerManager.configure_logger(LoggerConfig(output_dir=self.logging_dir))
        return self.experiment_definition

    def _setup_run(self) -> None:
        """
        Performs the necessary setup for creating a new run.
        This includes deleting old runs of this experiment, synchronizing threads if multi-threaded
        and loading django related application code.
        :return:
        """
        if TraceAccelerator.is_main_process:
            FileUtil.delete_dir(self.experiment_dir)
        TraceAccelerator.wait_for_everyone()
        get_wsgi_application()
