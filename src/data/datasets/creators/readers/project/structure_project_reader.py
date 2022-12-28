from typing import Dict

from data.datasets.creators.readers.project.iproject_reader import AbstractTraceProjectReader
from data.datasets.keys.safa_format import SafaKeys
from util.json_util import JSONUtil


class StructureProjectReader(AbstractTraceProjectReader):

    def get_trace_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaKeys.TRACES])
        return self.definition[SafaKeys.TRACES]

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [SafaKeys.ARTIFACTS])
        return self.definition[SafaKeys.ARTIFACTS]

    def _get_definition_file_name(self) -> str:
        return "definition.json"
