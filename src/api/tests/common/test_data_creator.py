from typing import List

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.objects.artifact import Artifact

ARTIFACT_MOCK_CONTENT = "dummy-text"


class TestDataCreator:
    @staticmethod
    def create_artifacts(layer_id: str, bodies: List[str] = None, n_artifacts: int = None, content: str = ARTIFACT_MOCK_CONTENT,
                         extension: str = EMPTY_STRING) -> List[Artifact]:
        """
        Creates artifacts with given conditions.
        :param layer_id: The layer_id to associated with them.
        :param bodies: The bodies of the artifacts to assign. Otherwise, dummy text is used.
        :param n_artifacts: The number of artifacts to create.
        :param extension: The extension to given their title.
        :param content: Content to give each artifact.
        :return: Artifacts.
        """
        if bodies is None:
            assert n_artifacts is not None, "Expected n_artifacts or bodies to be defined."
            bodies = [content] * n_artifacts

        artifacts = [Artifact(id=f"{i}{extension}", content=body, layer_id=layer_id) for i, body in enumerate(bodies)]
        return artifacts
