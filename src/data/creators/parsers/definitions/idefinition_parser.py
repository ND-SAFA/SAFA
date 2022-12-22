import os
from abc import ABC, abstractmethod
from typing import Dict

from data.creators.parsers.artifact_parser import ArtifactParser
from data.creators.parsers.definitions.structure_keys import StructureKeys
from data.creators.parsers.trace_parser import TraceDefinition
from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink
from util.file_util import FileUtil
from util.uncased_dict import UncasedDict


class IDefinitionParser(ABC):
    def __init__(self, project_path: str, definition_file_reader=FileUtil.read_json_file, conversions={}):
        self.project_path = project_path
        self.definition_path = os.path.join(project_path, self.get_definition_file_name())
        self.definition = UncasedDict(definition_file_reader(self.definition_path))
        self.conversions = self.definition.get(StructureKeys.CONVERSIONS, conversions)

    @abstractmethod
    def get_definition_file_name(self) -> str:
        pass

    @abstractmethod
    def get_artifact_definitions(self) -> Dict[str, Dict]:
        pass

    @abstractmethod
    def get_trace_definitions(self) -> Dict[str, Dict]:
        pass

    def create(self) -> TraceDataset:
        name2artifacts = {}
        for artifact_name, artifact_definition in self.get_artifact_definitions().items():
            name2artifacts[artifact_name] = ArtifactParser(self.project_path,
                                                           artifact_definition,
                                                           conversions=self.conversions)

        trace_links: Dict[int, TraceLink] = {}
        for trace_matrix_name, trace_definition_json in self.get_trace_definitions().items():
            trace_definition = TraceDefinition(self.project_path, trace_definition_json, name2artifacts,
                                               conversions=self.conversions)
            trace_links.update(trace_definition.create())
        return TraceDataset(links=trace_links)
