from common_resources.tools.util.supported_enum import SupportedEnum
from tgen.data.github.abstract_github_entity import AbstractGithubArtifact
from tgen.data.github.gartifacts.gartifact_type import GArtifactType
from tgen.data.github.gartifacts.gcode_file import GCodeFile
from tgen.data.github.gartifacts.gcommit import GCommit
from tgen.data.github.gartifacts.gissue import GIssue
from tgen.data.github.gartifacts.gpull import GPull
from tgen.data.github.gtraces.glink import GLink


class SupportedGArtifacts(SupportedEnum):
    """
    Enumeration of supported github artifacts.
    """
    LINK = GLink
    COMMIT = GCommit
    ISSUE = GIssue
    PULL = GPull
    CODE = GCodeFile

    @classmethod
    def get_value(cls, artifact_type: GArtifactType) -> AbstractGithubArtifact:
        """
        Returns the class associated with given github artifact.
        :param artifact_type: The type of github artifact.
        :return: The class constructor of given artifact type.
        """
        return super().get_value(artifact_type.name)
