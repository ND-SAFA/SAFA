import os
from abc import ABC, abstractmethod
from typing import Dict

from data.datasets.creators.readers.entity.artifact_reader import ArtifactReader
from data.datasets.creators.readers.entity.trace_entity_reader import TraceEntityReader
from data.datasets.keys.structure_keys import StructureKeys
from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink
from util.file_util import FileUtil
from util.uncased_dict import UncasedDict


class AbstractTraceProjectReader(ABC):
    """
    Responsible for reading artifacts and trace links and constructing
    a trace dataset.
    """

    def __init__(self, project_path: str, conversions=None):
        """
        Creates reader for project at path and column conversions given.
        :param project_path: Path to the project.
        :param conversions: Column conversions available to project.
        """
        if conversions is None:
            conversions = {}
        self.project_path = project_path
        self.definition = self._read_definition()
        self.conversions = self.definition.get(StructureKeys.CONVERSIONS, conversions)

    @abstractmethod
    def _get_definition_file_name(self) -> str:
        """
        Returns the name of the project's definition file to read.
        :return: Name of file.
        """

    @abstractmethod
    def get_artifact_definitions(self) -> Dict[str, Dict]:
        """
        Returns project's artifact definitions.
        :return: Artifact name to definition mapping.
        """

    @abstractmethod
    def get_trace_definitions(self) -> Dict[str, Dict]:
        """
        Returns project's trace definitions.
        :return: Mapping of trace matrix name to its trace defintion.
        """

    def create(self) -> TraceDataset:
        name2artifacts = self._create_artifact_readers(self.project_path, self.get_artifact_definitions())
        trace_links = self._create_trace_links(name2artifacts)
        return TraceDataset(links=trace_links)

    def _create_trace_links(self, name2artifacts: Dict[str, ArtifactReader]) -> Dict[int, TraceLink]:
        """
        Uses trace readers to extract project links.
        :param name2artifacts: Mapping between artifact name and its reader.
        :return: List of trace links found in project.
        """
        trace_links: Dict[int, TraceLink] = {}
        for trace_matrix_name, trace_definition_json in self.get_trace_definitions().items():
            trace_definition = TraceEntityReader(self.project_path, trace_definition_json, name2artifacts,
                                                 conversions=self.conversions)
            trace_links.update(trace_definition.get_entities())
        return trace_links

    def _create_artifact_readers(self, project_path: str, name2definition: Dict[str, Dict]) -> Dict[
        str, ArtifactReader]:
        """
        Creates artifact reader for each artifact definition.
        :param project_path: Path to project.
        :param name2definition: Mapping between artifacts' name and definition.
        :return:  Mapping between artifacts' name and its reader.
        """
        name2artifacts = {}
        for artifact_name, artifact_definition in name2definition.items():
            name2artifacts[artifact_name] = ArtifactReader(project_path,
                                                           artifact_definition,
                                                           conversions=self.conversions)
        return name2artifacts

    def _read_definition(self, definition_file_reader=FileUtil.read_json_file) -> UncasedDict:
        """
        Reads the project's definition file.
        :param definition_file_reader: The reader to convert file path to content.
        :return: Dictionary representing project definition.
        """
        definition_path = os.path.join(self.project_path, self._get_definition_file_name())
        definition_content = definition_file_reader(definition_path)
        return UncasedDict(definition_content)
