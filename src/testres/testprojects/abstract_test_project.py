from abc import abstractmethod
from typing import Dict, List


class AbstractTestProject:
    @property
    @abstractmethod
    def project_path(self) -> str:
        """
        :return: Path to the test project.
        """

    @abstractmethod
    def get_artifact_entries(self) -> List[Dict]:
        """
        :return: Returns artifact entries present in project.
        """

    @abstractmethod
    def get_trace_entries(self) -> List[Dict]:
        """
        :return: Returns trace entries in project.
        """

    @abstractmethod
    def get_layer_mapping_entries(self) -> List[Dict]:
        """
        :return: Returns layer mapping entries in project.
        """
