from typing import Dict, List, TypedDict

from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.serializers.artifact_serializer import ArtifactSerializer
from tgen.common.artifact import Artifact


class ProjectSummaryRequest(TypedDict):
    """
    The request to summarize a project.
    """
    artifacts: List[Artifact]


class ProjectSummarySerializer(AbstractSerializer):
    artifacts = ArtifactSerializer(many=True, help_text="Artifact map of all the artifacts in the system.")

    def create(self, validated_data: Dict) -> ProjectSummaryRequest:
        return ProjectSummaryRequest(artifacts=validated_data["artifacts"])
