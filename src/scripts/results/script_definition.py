import os
from typing import Any, Dict, List, Tuple

from util.file_util import FileUtil
from util.json_util import JsonUtil

ENV_REPLACEMENT_VARIABLES = ["DATA_PATH", "ROOT_PATH", "OUTPUT_PATH"]


class ScriptDefinition:
    """
    Contains functionality for reading and applying transformations to experiment definition.
    """
    MODELS_DIR_NAME = "models"
    LOG_DIR_NAME = "logs"
    JOB_DIR_NAME = "jobs"
    LOGGING_DIR_PARAM = "logging_dir"
    OUTPUT_DIR_PARAM = "output_dir"
    ENV_OUTPUT_PARMA = "[OUTPUT_PATH]"

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
        if os.path.isfile(definition_path):
            raise ValueError(f"{definition_path} does not exists.")

        definition_path = os.path.expanduser(definition_path)
        env_replacements = ScriptDefinition.get_env_replacements(env_replacements)
        job_definition = JsonUtil.read_json_file(definition_path)

        script_name = ScriptDefinition.get_script_name(definition_path)
        job_definition = ScriptDefinition.set_output_paths(job_definition, script_name)
        result = FileUtil.expand_paths_in_dictionary(job_definition, env_replacements)
        return result

    @staticmethod
    def set_output_paths(script_definition: Dict, script_name: str) -> Dict:
        """
        Sets the output path for the job results, logger, and model base dir.
        :param script_definition: The script definition to set output paths of.
        :param script_name: The name of the script.
        :return: Script definition with output paths modifications.
        """
        script_output_path = os.path.join(ScriptDefinition.ENV_OUTPUT_PARMA, script_name)
        script_definition[ScriptDefinition.OUTPUT_DIR_PARAM] = script_output_path
        script_definition[ScriptDefinition.LOGGING_DIR_PARAM] = script_output_path
        script_definition = ScriptDefinition.set_object_property(
            ("trainer_args", ScriptDefinition.OUTPUT_DIR_PARAM, script_output_path),
            script_definition)
        return script_definition

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

    @staticmethod
    def set_object_property(object_properties: Tuple[str, str, Any], object_data: Dict) -> Dict:
        """
        Replaces property in object with new value.
        :param object_properties: Object name, property name, and new property value.
        :param object_data: The dictionary whose sub object property will be replaced.
        :return: The object dictionary with modification.
        """
        if isinstance(object_data, str) or isinstance(object_data, float) or isinstance(object_data, int):
            return object_data

        object_name, prop_name, new_prop_value = object_properties
        new_obj = {}
        for k, v in object_data.items():
            if k == object_name and isinstance(v, dict):
                v = {**v, prop_name: new_prop_value}
            if isinstance(v, dict):
                v = ScriptDefinition.set_object_property(object_properties, v)
            if isinstance(v, list):
                v = [ScriptDefinition.set_object_property(object_properties, v_child) for v_child in v]
            new_obj[k] = v
        return new_obj

    @staticmethod
    def get_script_name(script_path: str):
        """
        Returns the name of the file referenced in path.
        :param script_path: Path to script file whose name is returned.
        :return: The name of the script.
        """
        path_without_extension, _ = os.path.splitext(script_path)
        _, file_name = os.path.split(path_without_extension)
        return file_name
