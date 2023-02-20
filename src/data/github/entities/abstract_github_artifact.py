from abc import ABC, abstractmethod
from typing import Dict, Union


class AbstractGithubArtifact(ABC):
    """
    Represents abstract repository artifact.
    """

    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Returns the dictionary containing artifact id and content.
        :return: Dataframe entry as dictionary.
        """
        pass

    @staticmethod
    @abstractmethod
    def read(row: Dict) -> "AbstractGithubArtifact":
        """
        Reads DataFrame row as artifact.
        :param row: The row in the dataframe.
        :return: The constructed artifact.
        """
        pass

    @abstractmethod
    def export(self, **kwargs) -> Union[Dict, None]:
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
        return str(self.to_dict())
