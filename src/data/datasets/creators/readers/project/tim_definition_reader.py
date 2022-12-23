from typing import Dict

from data.creators.readers.project.iproject_reader import IProjectParser
from data.creators.readers.project.structure_keys import StructureKeys
from data.formats.safa_format import SafaFormat
from util.file_util import FileUtil
from util.json_util import JSONUtil


class TimProjectReader(IProjectParser):
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

    def read_definition(self, definition_file_reader=FileUtil.read_json_file) -> Dict:
        definition = super().read_definition(definition_file_reader)
        return definition.rename_property(SafaFormat.FILE, StructureKeys.PATH)

    def get_definition_file_name(self) -> str:
        return "tim.json"

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaFormat.DATAFILES_KEY])
        artifact_definitions = self.definition[SafaFormat.DATAFILES_KEY]
        for artifact_name, artifact_definition in artifact_definitions.items():
            col_conversion_name = self.get_file_format(artifact_definition[SafaFormat.FILE])
            artifact_definition[StructureKeys.COLS] = "-".join([col_conversion_name, "artifacts"])
        return artifact_definitions

    def get_trace_definitions(self) -> Dict[str, Dict]:
        self.definition.pop(SafaFormat.DATAFILES_KEY)

        def get_column_conversion(trace_definition):
            file_format = self.get_file_format(trace_definition[StructureKeys.PATH])
            return "-".join([file_format, "traces"])

        return {
            key: {
                StructureKeys.PATH: definition[StructureKeys.PATH],
                StructureKeys.Trace.SOURCE: definition[SafaFormat.SOURCE_ID],
                StructureKeys.Trace.TARGET: definition[SafaFormat.TARGET_ID],
                StructureKeys.COLS: get_column_conversion(definition)
            }
            for key, definition in self.definition.items()
        }

    def get_file_format(self, file_path: str):
        supported_formats = ["csv", "json"]
        for format_name in supported_formats:
            format_id = "." + format_name
            if format_id in file_path:
                return format_name
        raise Exception(file_path, "did not have a supported format:", supported_formats)
