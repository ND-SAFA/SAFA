from dataclasses import dataclass
from typing import List, TypedDict

from rest_framework import serializers

from tgen.data.chunkers.supported_chunker import SupportedChunker


class SummaryArtifactPayload(TypedDict):
    """
    Type of summary artifact.
    """
    id: str
    name: str
    content: str
    type: str


@dataclass
class SummarizePayload:
    artifacts: List[SummaryArtifactPayload]


class SummaryArtifactSerializer(serializers.Serializer):
    """
    Serializes a summary artifact request.
    """
    id = serializers.CharField(max_length=100000, help_text="The id of the artifact.")
    name = serializers.CharField(max_length=100000, help_text="The name of the artifact.")
    content = serializers.CharField(max_length=100000, help_text="The content to summarize.")
    type = serializers.ChoiceField(choices=[(e.name, e.value) for e in SupportedChunker],
                                   help_text="The type of chunker to use for segmenting document.")

    def create(self, validated_data):
        return SummaryArtifactPayload(
            id=validated_data["id"],
            name=validated_data["name"],
            content=validated_data["content"],
            type=validated_data["type"]
        )


class SummarizeSerializer(serializers.Serializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = SummaryArtifactSerializer(many=True, help_text="Artifact information for summarization.")

    def create(self, validated_data):
        summary_serializer = SummaryArtifactSerializer(many=True, data=validated_data["artifacts"])
        summary_serializer.is_valid(raise_exception=True)
        summary_artifacts = summary_serializer.save()
        return SummarizePayload(artifacts=summary_artifacts)
