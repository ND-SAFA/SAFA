from typing import Dict, Union

from data.github.abstract_github_entity import AbstractGithubArtifact


class GLink(AbstractGithubArtifact):
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
    def read(row: Dict) -> "GLink":
        return GLink(row["source_id"], row["target_id"])

    def to_dict(self) -> Dict:
        return {
            "source_id": self.source,
            "target_id": self.target
        }
