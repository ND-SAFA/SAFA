from dataclasses import dataclass
from typing import List, TypedDict

from rest_framework import serializers

from api.endpoints.serializers.artifact_serializer import ArtifactSerializer


class SummaryArtifactPayload(TypedDict):
    """
    Type of summary artifact.
    """
    id: str
    name: str
    content: str
    type: str


@dataclass
class SummarizeRequest:
    artifacts: List[SummaryArtifactPayload]


MAX_LENGTH = 10 ** 10


class SummarizeSerializer(serializers.Serializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = ArtifactSerializer(many=True, help_text="Artifact information for summarization.")

    def create(self, validated_data):
        summary_serializer = ArtifactSerializer(many=True, data=validated_data["artifacts"])
        summary_serializer.is_valid(raise_exception=True)
        summary_artifacts = summary_serializer.save()
        return SummarizeRequest(artifacts=summary_artifacts)
