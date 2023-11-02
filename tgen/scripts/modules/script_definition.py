import os
from typing import Any, Dict, List, Tuple

from tgen.common.constants.path_constants import OUTPUT_PATH_PARAM
from tgen.common.util.file_util import ENV_REPLACEMENT_VARIABLES, FileUtil
from tgen.common.util.json_util import JsonUtil


class ScriptDefinition:
    """
    Contains functionality for reading and applying transformations to experiment definition.
    """
    LOGGING_DIR_PARAM = "logging_dir"
    OUTPUT_DIR_PARAM = "output_dir"
    ENV_OUTPUT_PARAM = f"[{OUTPUT_PATH_PARAM}]"

    @staticmethod
    def read_experiment_definition(definition_path: str, env_replacements: Dict = None,
                                   default_variables: List[str] = ENV_REPLACEMENT_VARIABLES) -> Dict:
        """
        Reads the experiment definition and applies env replacements.
        :param definition_path: Path to experiment jobs.
        :param env_replacements: Replacements to use instead of those defined by ENV.
        :param default_variables: List of env variables to include in replacements.
        :return: Processed definition.
        """
        if env_replacements is None:
            env_variables = ENV_REPLACEMENT_VARIABLES
            env_replacements = FileUtil.get_env_replacements(env_variables)
        if not os.path.isfile(definition_path):
            raise ValueError(f"{definition_path} does not exists.")

        definition_path = os.path.expanduser(definition_path)

        job_definition = JsonUtil.read_json_file(definition_path)

        script_name = ScriptDefinition.get_script_name(definition_path)
        job_definition = ScriptDefinition.set_output_paths(job_definition, script_name)
        result = FileUtil.expand_paths(job_definition, env_replacements, use_abs_paths=False)
        return result

    @staticmethod
    def set_output_paths(script_definition: Dict, script_name: str) -> Dict:
        """
        Sets the output path for the job results, logger, and model base dir.
        :param script_definition: The script definition to set output paths of.
        :param script_name: The name of the script.
        :return: Script definition with output paths modifications.
        """

        if ScriptDefinition.OUTPUT_DIR_PARAM not in script_definition:
            script_output_path = os.path.join(ScriptDefinition.ENV_OUTPUT_PARAM, script_name)
        else:
            script_output_path = script_definition[ScriptDefinition.OUTPUT_DIR_PARAM]
        script_output_path = os.path.expanduser(script_output_path)
        script_definition[ScriptDefinition.OUTPUT_DIR_PARAM] = script_output_path
        # script_definition[ScriptDefinition.LOGGING_DIR_PARAM] = script_output_path
        script_definition = ScriptDefinition.set_object_property(
            ("trainer_args", ScriptDefinition.OUTPUT_DIR_PARAM, script_output_path),
            script_definition)
        return script_definition

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
    def get_script_name(path: str) -> str:
        """
        :param path: Path used to construct id.
        :return: Returns the directory and file name of path used to identify scripts.
        """
        return FileUtil.get_file_name(path, n_parents=1)
