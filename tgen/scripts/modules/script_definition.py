import os
from typing import Any, Dict, Tuple

from tgen.common.constants.path_constants import OUTPUT_PATH_PARAM
from tgen.scripts.toolset.rq_definition import RQDefinition


class ScriptDefinition:
    """
    Contains functionality for reading and applying transformations to experiment definition.
    """
    LOGGING_DIR_PARAM = "logging_dir"
    OUTPUT_DIR_PARAM = "output_dir"
    ENV_OUTPUT_PARAM = f"[{OUTPUT_PATH_PARAM}]"

    @staticmethod
    def read_experiment_definition(definition_path: str = None, rq_definition: RQDefinition = None,
                                   env_replacements: Dict = None) -> Dict:
        """
        Reads the experiment definition and applies env replacements.
        :param definition_path: Path to experiment jobs.
        :param env_replacements: Replacements to use instead of those defined by ENV.
        :param default_variables: List of env variables to include in replacements.
        :return: Processed definition.
        """
        if definition_path:
            rq_definition = RQDefinition(definition_path)

        if not rq_definition:
            raise Exception("Expected definition path or rq definition to be given.")

        rq_definition_json = rq_definition.build_rq(error_on_fail=True)
        rq_definition_json = ScriptDefinition.set_output_paths(rq_definition_json, rq_definition.script_name)

        return rq_definition_json

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
