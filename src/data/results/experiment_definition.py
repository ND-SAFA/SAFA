import os
from typing import Dict, List

from util.file_util import FileUtil
from util.json_util import JsonUtil

ENV_REPLACEMENT_VARIABLES = ["DATA_PATH", "ROOT_PATH", "OUTPUT_PATH"]


class ExperimentDefinition:
    """
    Contains functionality for reading and applying transformations to experiment definition.
    """

    @staticmethod
    def read_experiment_definition(definition_path: str, env_replacements: List[str] = None) -> Dict:
        """
        Reads the experiment definition and applies env replacements.
        :param definition_path: Path to experiment jobs.
        :param env_replacements: List of environment variables to replace in definition.
        :return: Processed definition.
        """
        if env_replacements is None:
            env_replacements = ENV_REPLACEMENT_VARIABLES
        definition_path = os.path.expanduser(definition_path)
        env_replacements = ExperimentDefinition.get_env_replacements(env_replacements)
        job_definition = JsonUtil.read_json_file(definition_path)
        result = FileUtil.expand_paths_in_dictionary(job_definition, env_replacements)
        return result

    @staticmethod
    def get_env_replacements(env_variables: List[str]) -> Dict[str, str]:
        """
        :return: Dictionary of environment variables to their values.
        """
        replacements = {}
        for replacement_path in env_variables:
            path_value = os.environ.get(replacement_path, None)
            if path_value:
                path_key = "[%s]" % replacement_path
                replacements[path_key] = os.path.expanduser(path_value)
        return replacements
