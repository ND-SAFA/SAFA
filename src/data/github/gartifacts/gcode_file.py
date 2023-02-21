from typing import Dict, Union

from data.github.abstract_github_entity import AbstractGithubArtifact


class GCodeFile(AbstractGithubArtifact):

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self.read_file_content(self.file_path)

    def to_dict(self) -> Dict:
        return self.export()

    @staticmethod
    def read(row: Dict) -> "AbstractArtifact":
        raise NotImplementedError

    def export(self, **kwargs) -> Union[Dict, None]:
        return {"id": self.get_id(), "content": self.content}

    def get_id(self) -> str:
        return self.file_path

    @staticmethod
    def read_file_content(file_path: str) -> str:
        with open(file_path, "r+") as code_file:
            content = code_file.read()
        return content
