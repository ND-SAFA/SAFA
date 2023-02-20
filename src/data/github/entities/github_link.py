from typing import Dict, Union

from data.github.entities.abstract_github_artifact import AbstractGithubArtifact


class Link(AbstractGithubArtifact):
    """
    Represent link between repository artifacts.
    """

    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def export(self, **kwargs) -> Union[Dict, None]:
        return {"source": self.source, "target": self.target}

    def get_id(self) -> str:
        return str(self.source) + "~" + str(self.target)

    @staticmethod
    def read(row: Dict) -> "Link":
        return Link(row["source_id"], row["target_id"])

    def to_dict(self) -> Dict:
        return {
            "source_id": self.source,
            "target_id": self.target
        }
