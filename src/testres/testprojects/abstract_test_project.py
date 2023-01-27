from abc import abstractmethod
from typing import Dict, List

from data.readers.abstract_project_reader import AbstractProjectReader
from testres.testprojects.entry_creator import LayerEntry


class AbstractTestProject:
    """
    Represents interface for defining a test project to create assertions for.
    """

    @staticmethod
    @abstractmethod
    def get_project_path() -> str:
        """
        :return: Path to the test project.
        """

    @classmethod
    @abstractmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns project reader for project.
        """

    @staticmethod
    @abstractmethod
    def get_source_entries() -> List[LayerEntry]:
        """
        :return: Returns the source artifact entries per artifact layer.
        """

    @staticmethod
    @abstractmethod
    def get_target_entries() -> List[LayerEntry]:
        """
        :return: Returns the target artifact entries per artifact layer.
        """

    @classmethod
    @abstractmethod
    def get_trace_entries(cls) -> LayerEntry:
        """
        :return: Returns trace entries in project.
        """

    @classmethod
    @abstractmethod
    def get_layer_mapping_entries(cls) -> List[Dict]:
        """
        :return: Returns layer mapping entries in project.
        """

    @classmethod
    def get_artifact_entries(cls) -> List[Dict]:
        """
        :return: Returns artifact entries present in project.
        """
        sources = []
        targets = []
        for source_features, target_features in zip(cls.get_source_entries(), cls.get_target_entries()):
            sources.extend(source_features)
            targets.extend(target_features)
        return sources + targets  # matches the order of the datasets

    @staticmethod
    @abstractmethod
    def get_n_links() -> int:
        """
        :return: Returns the number of expected links after construction.
        """

    @classmethod
    @abstractmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns the number of positive links in project.
        """
