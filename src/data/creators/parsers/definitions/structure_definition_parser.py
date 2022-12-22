from typing import Dict

from data.creators.parsers.definitions.idefinition_parser import IDefinitionParser
from data.formats.safa_format import SafaFormat
from util.json_util import JSONUtil


class StructureDefinitionParser(IDefinitionParser):

    def get_trace_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaFormat.TRACES])
        return self.definition[SafaFormat.TRACES]

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaFormat.ARTIFACTS])
        return self.definition[SafaFormat.ARTIFACTS]

    def get_definition_file_name(self) -> str:
        return "definition.json"
