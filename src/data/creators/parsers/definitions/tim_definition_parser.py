from typing import Dict

from data.creators.parsers.definitions.idefinition_parser import IDefinitionParser
from data.creators.parsers.definitions.structure_keys import StructureKeys
from data.formats.safa_format import SafaFormat
from util.json_util import JSONUtil


class TimDefinitionParser(IDefinitionParser):
    def __init__(self, project_path: str):
        super().__init__(project_path, conversions={
            "traces": {
                "sourceName": "source",
                "targetName": "target"
            }, "artifacts": {
                "name": "id",
                "body": "content",
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
            artifact_definition[StructureKeys.COLS] = "artifacts"
        return artifact_definitions

    def get_trace_definitions(self) -> Dict[str, Dict]:
        self.definition.pop(SafaFormat.DATAFILES_KEY)
        return {
            key: {
                "file": definition["File"],
                "source": definition["Source"],
                "target": definition["Target"],
                "cols": "traces"
            }
            for key, definition in self.definition.items()
        }
