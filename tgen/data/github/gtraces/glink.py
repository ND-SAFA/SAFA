from typing import Dict, Union

from common_resources.tools.constants.symbol_constants import USER_SYM

from common_resources.tools.util.override import overrides
from tgen.data.github.abstract_github_entity import AbstractGithubArtifact


class GLink(AbstractGithubArtifact):
    """
    Represent link between repository artifacts.
    """

    def __init__(self, source: str, target: str):
        """
        Creates links between source and target artifact ids.
        :param source: The source artifact id.
        :param target: The target artifact id.
        """
        self.source = source
        self.target = target

    @overrides(AbstractGithubArtifact)
    def as_dataframe_entry(self, **kwargs) -> Union[Dict, None]:
        """
        Returns DataFrame entity of link for exporting.
        :param kwargs: Additional arguments to customize exporting. None used currently.
        :return: Dictionary to be used as data frame entry.
        """
        return {"source": self.source, "target": self.target}

    @overrides(AbstractGithubArtifact)
    def get_id(self) -> str:
        """
        :return: Returns the trace link id between source and target.
        """
        return str(self.source) + USER_SYM + str(self.target)

    @overrides(AbstractGithubArtifact)
    def get_state_dict(self) -> Dict:
        """
        :return: Returns the dictionary used to write state to disk.
        """
        return {
            "source_id": self.source,
            "target_id": self.target
        }

    @staticmethod
    @overrides(AbstractGithubArtifact)
    def from_state_dict(state_dict: Dict) -> "GLink":
        """
        Creates GLink from entry written to disk.
        :param state_dict: The row of the data frame to initialize from.
        :return: Constructed GLink.
        """
        return GLink(state_dict["source_id"], state_dict["target_id"])
