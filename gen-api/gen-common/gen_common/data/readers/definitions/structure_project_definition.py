import os
from typing import Dict

from gen_common.data.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from gen_common.util.json_util import JsonUtil


class StructureProjectDefinition(AbstractProjectDefinition):
    """
    Defines how to read the definition for a structured project.
    """
    STRUCTURE_DEFINITION_FILE_NAME = "definition.json"

    @staticmethod
    def read_project_definition(project_path: str) -> Dict:
        """
        Reads the project definition for a structured project.
        :param project_path: Path to project to read.
        :return: Dict representing content of project definition.
        """
        definition_path = os.path.join(project_path, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)
        return JsonUtil.read_json_file(definition_path)
