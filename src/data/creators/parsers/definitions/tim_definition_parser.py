from typing import Dict

from data.creators.parsers.definitions.idefinition_parser import IDefinitionParser
from data.creators.parsers.definitions.structure_keys import StructureKeys
from data.formats.safa_format import SafaFormat
from util.json_util import JSONUtil


class TimDefinitionParser(IDefinitionParser):
    def __init__(self, project_path: str):
        super().__init__(project_path, conversions={
            "json-traces": {
                "sourceName": "source",
                "targetName": "target"
            },
            "csv-traces": {
                "source": "source",
                "target": "target"
            },
            "json-artifacts": {
                "name": "id",
                "body": "content"
            },
            "csv-artifacts": {
                "id": "id",
                "content": "content"
            }
        })

    def get_definition_file_name(self) -> str:
        return "tim.json"

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaFormat.DATAFILES_KEY])
        artifact_definitions = self.definition[SafaFormat.DATAFILES_KEY]
        for artifact_name, artifact_definition in artifact_definitions.items():
            col_conversion_name = self.get_file_format(artifact_definition[StructureKeys.FILE])
            artifact_definition[StructureKeys.COLS] = "-".join([col_conversion_name, "artifacts"])
        return artifact_definitions

    def get_trace_definitions(self) -> Dict[str, Dict]:
        self.definition.pop(SafaFormat.DATAFILES_KEY)

        def get_conversion_name(trace_definition):
            return "-".join([self.get_file_format(trace_definition[StructureKeys.FILE]), "traces"])

        return {
            key: {
                "file": definition["File"],
                "source": definition["Source"],
                "target": definition["Target"],
                "cols": get_conversion_name(definition)
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
