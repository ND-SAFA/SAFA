from typing import Dict

from data.datasets.creators.readers.project.iproject_reader import AbstractTraceProjectReader
from data.datasets.keys.structure_keys import StructureKeys
from util.json_util import JSONUtil


class StructureProjectReader(AbstractTraceProjectReader):

    def get_trace_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [StructureKeys.TRACES])
        return self.definition[StructureKeys.TRACES]

    def get_artifact_definitions(self) -> Dict[str, Dict]:
        JSONUtil.require_properties(self.definition, [StructureKeys.ARTIFACTS])
        return self.definition[StructureKeys.ARTIFACTS]

    def _get_definition_file_name(self) -> str:
        return "definition.json"
