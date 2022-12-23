from typing import Dict

from data.datasets.creators.readers.project.iproject_reader import IProjectParser
from data.datasets.formats.safa_format import SafaFormat
from util.json_util import JSONUtil


class StructureProjectReader(IProjectParser):

    def get_trace_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaFormat.TRACES])
        return self.definition[SafaFormat.TRACES]

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaFormat.ARTIFACTS])
        return self.definition[SafaFormat.ARTIFACTS]

    def get_definition_file_name(self) -> str:
        return "definition.json"
