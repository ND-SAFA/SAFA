import os
from typing import Dict

from gen_common.constants import NO_CHECK, PERIOD
from gen_common.data.keys.safa_keys import SafaKeys
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from gen_common.util.json_util import JsonUtil


class TimProjectDefinition(AbstractProjectDefinition):
    """
    Responsible for converting the definition for a SAFA project into the structured project format.
    """
    CSV = "csv"
    JSON = "json"
    CONVERSIONS = {
        JSON: {
            StructuredKeys.ARTIFACTS: {
                "name": StructuredKeys.Artifact.ID.value,
                "body": StructuredKeys.Artifact.CONTENT.value,
                "summary": StructuredKeys.Artifact.SUMMARY.value
            },
            StructuredKeys.TRACES: {
                "sourceName": StructuredKeys.Trace.SOURCE.value,
                "targetName": StructuredKeys.Trace.TARGET.value,
                "score": StructuredKeys.Trace.SCORE.value,
                "explanation": StructuredKeys.Trace.EXPLANATION.value
            }
        },
        CSV: {
            StructuredKeys.ARTIFACTS: {
                "id": StructuredKeys.Artifact.ID.value,
                "content": StructuredKeys.Artifact.CONTENT.value,
                "summary": StructuredKeys.Artifact.SUMMARY.value
            },
            StructuredKeys.TRACES: {
                "source": StructuredKeys.Trace.SOURCE.value,
                "target": StructuredKeys.Trace.TARGET.value,
                "label": StructuredKeys.Trace.LABEL.value,
                "score": StructuredKeys.Trace.SCORE.value,
                "explanation": StructuredKeys.Trace.EXPLANATION.value
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
        tim_file = JsonUtil.read_json_file(tim_file_path)
        artifact_definitions = TimProjectDefinition._create_artifact_definitions(tim_file)
        trace_definitions = TimProjectDefinition._create_trace_definitions(tim_file)
        return {
            StructuredKeys.ARTIFACTS: artifact_definitions,
            StructuredKeys.TRACES: trace_definitions,
            StructuredKeys.CONVERSIONS: TimProjectDefinition.get_flattened_conversions(),
            StructuredKeys.OVERRIDES: {
                "allowed_orphans": NO_CHECK
            }
        }

    @staticmethod
    def _create_artifact_definitions(definition: Dict) -> Dict[str, Dict]:
        """
        Creates artifact definitions from project definition in structure project format.
        :param definition: The project definition
        :return: Mapping between artifact type to its definition.
        """
        JsonUtil.require_properties(definition, [SafaKeys.ARTIFACTS])
        artifact_definitions = definition[SafaKeys.ARTIFACTS]
        artifact_definitions_map = {}
        for artifact_definition in artifact_definitions:
            JsonUtil.require_properties(artifact_definition, [SafaKeys.TYPE, SafaKeys.FILE])
            artifact_type = artifact_definition.pop(SafaKeys.TYPE)
            artifact_data_path = artifact_definition.pop(SafaKeys.FILE)
            col_conversion_name = TimProjectDefinition.get_file_format(artifact_data_path)
            artifact_definition[StructuredKeys.PATH] = artifact_data_path
            artifact_definition[StructuredKeys.COLS] = TimProjectDefinition.get_conversion_id(col_conversion_name,
                                                                                              StructuredKeys.ARTIFACTS)
            artifact_definitions_map[artifact_type] = artifact_definition
        return artifact_definitions_map

    @staticmethod
    def _create_trace_definitions(project_definition: Dict) -> Dict[str, Dict]:
        """
        Creates trace definitions from project definition in structure project format.
        :param project_definition: The project definition.
        :return: Mapping of trace matrix name to its definition.
        """
        JsonUtil.require_properties(project_definition, [SafaKeys.TRACES])
        definitions = project_definition.pop(SafaKeys.TRACES)

        trace_definitions_map = {}
        for t_definition in definitions:
            JsonUtil.require_properties(t_definition, [SafaKeys.FILE, SafaKeys.SOURCE_ID, SafaKeys.TARGET_ID])
            source_type = t_definition[SafaKeys.SOURCE_ID]
            target_type = t_definition[SafaKeys.TARGET_ID]
            t_file = t_definition[SafaKeys.FILE]
            trace_definition_key = f"{source_type}2{target_type}"
            trace_definitions_map[trace_definition_key] = {
                StructuredKeys.PATH: t_file,
                StructuredKeys.Trace.SOURCE.value: source_type,
                StructuredKeys.Trace.TARGET.value: target_type,
                StructuredKeys.COLS: TimProjectDefinition.get_conversion_id(
                    TimProjectDefinition.get_file_format(t_definition[SafaKeys.FILE]),
                    StructuredKeys.TRACES)
            }
        return trace_definitions_map

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
            format_id = PERIOD + format_name
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
