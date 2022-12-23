import os
from abc import ABC, abstractmethod
from typing import Dict

from data.datasets.trace_dataset import TraceDataset
from data.readers.artifact_reader import ArtifactReader
from data.readers.project.structure_keys import StructureKeys
from data.readers.trace_reader import TraceDefinition
from data.tree.trace_link import TraceLink
from util.file_util import FileUtil
from util.uncased_dict import UncasedDict


class IProjectParser(ABC):
    def __init__(self, project_path: str, conversions={}):
        self.project_path = project_path
        self.definition = self.read_definition()
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
        name2artifacts = self.create_artifact_parsers(self.project_path, self.get_artifact_definitions())
        trace_links = self.create_trace_links(name2artifacts)
        return TraceDataset(links=trace_links)

    def create_trace_links(self, name2artifacts: Dict[str, ArtifactReader]) -> Dict[int, TraceLink]:
        trace_links: Dict[int, TraceLink] = {}
        for trace_matrix_name, trace_definition_json in self.get_trace_definitions().items():
            trace_definition = TraceDefinition(self.project_path, trace_definition_json, name2artifacts,
                                               conversions=self.conversions)
            trace_links.update(trace_definition.get_entities())
        return trace_links

    def create_artifact_parsers(self, project_path: str, name2definition: Dict[str, Dict]) -> Dict[str, ArtifactReader]:
        name2artifacts = {}
        for artifact_name, artifact_definition in name2definition.items():
            name2artifacts[artifact_name] = ArtifactReader(project_path,
                                                           artifact_definition,
                                                           conversions=self.conversions)
        return name2artifacts

    def read_definition(self, definition_file_reader=FileUtil.read_json_file) -> UncasedDict:
        definition_path = os.path.join(self.project_path, self.get_definition_file_name())
        return UncasedDict(definition_file_reader(definition_path))
