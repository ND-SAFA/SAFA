from abc import abstractmethod
from typing import Dict, List

from testres.testprojects.entry_creator import LayerEntry


class AbstractTestProject:
    @property
    @abstractmethod
    def project_path(self) -> str:
        """
        :return: Path to the test project.
        """

    @staticmethod
    @abstractmethod
    def get_source_entries() -> List[LayerEntry]:
        pass

    @staticmethod
    @abstractmethod
    def get_target_entries() -> List[LayerEntry]:
        pass

    @abstractmethod
    def get_trace_entries(self) -> LayerEntry:
        """
        :return: Returns trace entries in project.
        """

    @abstractmethod
    def get_layer_mapping_entries(self) -> List[Dict]:
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

    @classmethod
    def get_n_links(cls) -> int:
        n_links = 0
        for source, targets in zip(cls.get_source_entries(), cls.get_target_entries()):
            n_links += len(source) * len(targets)
        return n_links

    @classmethod
    def get_n_positive_links(cls):
        return len(cls.get_trace_entries())
