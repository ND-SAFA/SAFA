import os
from typing import Dict, Type

from common_resources.tools.constants.env_var_name_constants import OUTPUT_PATH_PARAM

from tgen.common.constants.tgen_constants import WANDB_DIR_PARAM
from common_resources.tools.t_logging.logger_config import LoggerConfig
from common_resources.tools.t_logging.logger_manager import LoggerManager, logger
from common_resources.tools.util.file_util import FileUtil
from tgen.experiments.experiment import Experiment
from tgen.scripts.modules.experiment_types import ExperimentTypes
from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.modules.script_reader import ScriptOutputReader
from tgen.testres.object_creator import ObjectCreator


class ScriptRunner:
    """
    Responsible for reading/preprocessing script definition, running script, and reading results.
    ---
    Script Definition: JSON file definition experiment definition using any syntactic sugars.
    """
    FINISHED_HEADER = "Experiment Finished! :)"
    EXPERIMENT_TYPE_PARAM = "experiment_type"

    def __init__(self, script_definition_path: str):
        """
        Initializes runner for definition at path.
        :param script_definition_path: Path to the script definition defining experiment to open.
        """
        self.script_definition_path = script_definition_path
        self.experiment_definition = None
        self.experiment_dir = None
        self.logging_dir = None
        self.experiment = None
        os.environ[WANDB_DIR_PARAM] = os.path.join(os.path.expanduser(os.environ[OUTPUT_PATH_PARAM]))

    def run(self) -> None:
        """
        Runs experiment defined by definition
        :return: None
        """
        experiment = self.get_experiment()
        self._setup_run()
        LoggerManager.turn_off_hugging_face_logging()
        experiment.run()
        logger.info(self.FINISHED_HEADER)

    def print_results(self) -> None:
        """
        Prints the results of the experiment.
        :return:
        """
        self._load_experiment_definition()
        self.script_reader.print_val()
        self.script_reader.print_eval()

    def get_experiment(self) -> Experiment:
        """
        :return: Returns the script experiment.
        """
        if self.experiment is None:
            experiment_definition = self._load_experiment_definition()
            experiment_class = ScriptRunner.get_experiment_class(experiment_definition)
            self.experiment = ObjectCreator.create(experiment_class, override=True, **experiment_definition)
        return self.experiment

    def _load_experiment_definition(self) -> Dict:
        """
        Reads script definition.
        :return:
        """
        if self.experiment_definition is None:
            self.experiment_definition = ScriptDefinition.read_experiment_definition(self.script_definition_path)
            experiment_definition = self._load_experiment_definition()
            self.experiment_dir = experiment_definition[ScriptDefinition.OUTPUT_DIR_PARAM]
            self.logging_dir = os.path.join(experiment_definition[ScriptDefinition.OUTPUT_DIR_PARAM], "logs")
            LoggerManager.configure_logger(LoggerConfig(output_dir=self.logging_dir))
            self.script_reader = ScriptOutputReader(self.experiment_dir)
        return self.experiment_definition

    def _setup_run(self) -> None:
        """
        Performs the necessary setup for creating a new run.
        This includes deleting old runs of this experiment, synchronizing threads if multi-threaded
        and loading django related application code.
        :return:
        """
        if self.experiment.delete_prev_experiment_dir:
            FileUtil.delete_dir(self.experiment_dir)
            FileUtil.create_dir_safely(self.experiment_dir)

    @staticmethod
    def get_experiment_class(experiment_definition: Dict) -> Type[Experiment]:
        """
        Reads the current experiment type of definition.
        :param experiment_definition: The definitions of the experiment.
        :return: The experiment class defined in definition.
        """
        if ScriptRunner.EXPERIMENT_TYPE_PARAM in experiment_definition:
            experiment_class_name = experiment_definition.pop(ScriptRunner.EXPERIMENT_TYPE_PARAM)
        else:
            experiment_class_name = ExperimentTypes.BASE.name
        return ExperimentTypes.get_value(experiment_class_name)
