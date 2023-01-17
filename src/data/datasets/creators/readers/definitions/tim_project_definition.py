import os
from copy import deepcopy
from typing import Dict

from data.datasets.creators.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from data.datasets.keys.safa_format import SafaKeys
from data.datasets.keys.structure_keys import StructureKeys
from util.file_util import FileUtil
from util.json_util import JSONUtil


class TimProjectDefinition(AbstractProjectDefinition):
    """
    Responsible for converting the definition for a SAFA project into the structured project format.
    """
    CSV = "csv"
    JSON = "json"
    CONVERSIONS = {
        JSON: {
            StructureKeys.ARTIFACTS: {
                "name": StructureKeys.Artifact.ID,
                "body": StructureKeys.Artifact.BODY
            },
            StructureKeys.TRACES: {
                "sourceName": StructureKeys.Trace.SOURCE,
                "targetName": StructureKeys.Trace.TARGET,
            }
        },
        CSV: {
            StructureKeys.ARTIFACTS: {
                "id": StructureKeys.Artifact.ID,
                "content": StructureKeys.Artifact.BODY
            },
            StructureKeys.TRACES: {
                "source": StructureKeys.Trace.SOURCE,
                "target": StructureKeys.Trace.TARGET,
            }
        }
    }

    @staticmethod
    def read_project_definition(project_path: str) -> Dict:
        """
        Reads the Tim.json file and converts it into the structure project definition format.
        :param project_path: Path to safa project.
        :return: Dictionary representing project definition.
        """
        tim_file_path = os.path.join(project_path, SafaKeys.TIM_FILE)
        tim_file = FileUtil.read_json_file(tim_file_path)
        artifact_definitions = TimProjectDefinition._create_artifact_definitions(tim_file)
        trace_definitions = TimProjectDefinition._create_trace_definitions(tim_file)
        return {
            StructureKeys.ARTIFACTS: artifact_definitions,
            StructureKeys.TRACES: trace_definitions,
            StructureKeys.COLS: TimProjectDefinition.get_flattened_conversions()
        }

    @staticmethod
    def _create_artifact_definitions(definition: Dict) -> Dict[str, Dict]:
        """
        Creates artifact definitions from project definition in structure project format.
        :param definition: The project definition
        :return: Mapping between artifact type to its definition.
        """
        JSONUtil.require_properties(definition, [SafaKeys.DATAFILES_KEY])
        artifact_definitions = definition[SafaKeys.DATAFILES_KEY]
        for _, artifact_definition in artifact_definitions.items():
            col_conversion_name = TimProjectDefinition.get_file_format(artifact_definition[SafaKeys.FILE])
            artifact_definition[StructureKeys.COLS] = TimProjectDefinition.get_conversion_id(col_conversion_name,
                                                                                             StructureKeys.ARTIFACTS)
        return artifact_definitions

    @staticmethod
    def _create_trace_definitions(definition: Dict) -> Dict[str, Dict]:
        """
        Creates trace definitions from project definition in structure project format.
        :param definition: The project definition.
        :return: Mapping of trace matrix name to its definition.
        """
        definition = deepcopy(definition)
        definition.pop(SafaKeys.DATAFILES_KEY)
        file_format = TimProjectDefinition.get_file_format(definition[StructureKeys.PATH])

        return {
            key: {
                StructureKeys.PATH: definition[StructureKeys.PATH],
                StructureKeys.Trace.SOURCE: definition[SafaKeys.SOURCE_ID],
                StructureKeys.Trace.TARGET: definition[SafaKeys.TARGET_ID],
                StructureKeys.COLS: TimProjectDefinition.get_conversion_id(file_format, StructureKeys.TRACES)
            }
            for key, definition in definition.items()
        }

    @staticmethod
    def get_flattened_conversions() -> Dict[str, Dict]:
        """
        Returns column definitions for the safa project in the structure project format
        :return: Mapping of column conversion id to the conversion.
        """
        flattened_conversions = {}
        for k, v in TimProjectDefinition.CONVERSIONS.items():
            for k_inner, v_inner in v.items():
                new_key = TimProjectDefinition.get_conversion_id(k, k_inner)
                flattened_conversions[new_key] = v_inner
        return flattened_conversions

    @staticmethod
    def get_file_format(file_path: str) -> str:
        """
        Returns the format of the file.
        :param file_path: Path to file whose format is returned.
        :return: String representing name of format.
        """
        supported_formats = list(TimProjectDefinition.CONVERSIONS.keys())
        for format_name in supported_formats:
            format_id = "." + format_name
            if format_id in file_path:
                return format_name
        raise ValueError(file_path, "did not have a supported format:", supported_formats)

    @staticmethod
    def get_conversion_id(file_format: str, entity_type: str) -> str:
        """
        Returns the id of the column conversion to read entity type.
        :param file_format: The format of the file containing entities.
        :param entity_type: The type of entities to read.
        :return: String representing column conversion id.
        """
        return "-".join([file_format, entity_type])
