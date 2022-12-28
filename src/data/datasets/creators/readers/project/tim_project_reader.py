from typing import Dict

from data.datasets.creators.readers.project.iproject_reader import AbstractTraceProjectReader
from data.datasets.keys.safa_format import SafaKeys
from data.datasets.keys.structure_keys import StructureKeys
from util.file_util import FileUtil
from util.json_util import JSONUtil


class TimProjectReader(AbstractTraceProjectReader):
    def __init__(self, project_path: str):
        super().__init__(project_path, conversions={
            "json-traces": {
                "sourceName": StructureKeys.Trace.SOURCE,
                "targetName": StructureKeys.Trace.TARGET,
            },
            "csv-traces": {
                "source": StructureKeys.Trace.SOURCE,
                "target": StructureKeys.Trace.TARGET,
            },
            "json-artifacts": {
                "name": StructureKeys.Artifact.ID,
                "body": StructureKeys.Artifact.BODY
            },
            "csv-artifacts": {
                "id": StructureKeys.Artifact.ID,
                "content": StructureKeys.Artifact.BODY
            }
        })

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaKeys.DATAFILES_KEY])
        artifact_definitions = self.definition[SafaKeys.DATAFILES_KEY]
        for artifact_name, artifact_definition in artifact_definitions.items():
            col_conversion_name = self.get_file_format(artifact_definition[SafaKeys.FILE])
            artifact_definition[StructureKeys.COLS] = "-".join([col_conversion_name, "artifacts"])
        return artifact_definitions

    def get_trace_definitions(self) -> Dict[str, Dict]:
        self.definition.pop(SafaKeys.DATAFILES_KEY)

        def get_column_conversion(trace_definition):
            file_format = self.get_file_format(trace_definition[StructureKeys.PATH])
            return "-".join([file_format, "traces"])

        return {
            key: {
                StructureKeys.PATH: definition[StructureKeys.PATH],
                StructureKeys.Trace.SOURCE: definition[SafaKeys.SOURCE_ID],
                StructureKeys.Trace.TARGET: definition[SafaKeys.TARGET_ID],
                StructureKeys.COLS: get_column_conversion(definition)
            }
            for key, definition in self.definition.items()
        }

    def _read_definition(self, definition_file_reader=FileUtil.read_json_file) -> Dict:
        definition = super()._read_definition(definition_file_reader)
        return definition.rename_property(SafaKeys.FILE, StructureKeys.PATH)

    def _get_definition_file_name(self) -> str:
        return "tim.json"

    @staticmethod
    def get_file_format(file_path: str):
        supported_formats = ["csv", "json"]
        for format_name in supported_formats:
            format_id = "." + format_name
            if format_id in file_path:
                return format_name
        raise ValueError(file_path, "did not have a supported format:", supported_formats)
