from abc import ABC, abstractmethod
from typing import Dict, Union


class AbstractGithubArtifact(ABC):
    """
    Represents abstract repository artifact.
    """

    @abstractmethod
    def get_state_dict(self) -> Dict:
        """
        Returns the dictionary containing artifact id and content.
        :return: Dataframe entry as dictionary.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_state_dict(state_dict: Dict) -> "AbstractGithubArtifact":
        """
        Reads DataFrame row as artifact.
        :param state_dict: The row in the dataframe.
        :return: The constructed artifact.
        """
        pass

    @abstractmethod
    def as_dataframe_entry(self, **kwargs) -> Union[Dict, None]:
        """
        Exports artifact id and content.
        :param kwargs: Additional parameters for customizing what content to include.
        :return: DataFrame entry of artifact.
        """
        pass

    @abstractmethod
    def get_id(self) -> str:
        """
        :return: Returns the ID of the artifact.
        """
        pass

    def __str__(self):
        """
        :return: Returns artifact as export dictionary.
        """
        return str(self.get_state_dict())
