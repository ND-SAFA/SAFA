from typing import List, TypedDict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from tgen.data.chunkers.supported_chunker import SupportedChunker


class SummaryArtifactPayload(TypedDict):
    """
    Type of summary artifact.
    """
    id: str
    name: str
    content: str
    type: str


class SummarizePayload(TypedDict):
    artifacts: List[SummaryArtifactPayload]
    model: str
    prompt: str


class SummaryArtifactSerializer(AbstractSerializer):
    """
    Serializes a summary artifact request.
    """
    id = serializers.CharField(max_length=100000, help_text="The id of the artifact.")
    name = serializers.CharField(max_length=100000, help_text="The name of the artifact.")
    content = serializers.CharField(max_length=100000, help_text="The content to summarize.")
    type = serializers.ChoiceField(choices=[(e.name, e.value) for e in SupportedChunker],
                                   help_text="The type of chunker to use for segmenting document.")


class SummarizeSerializer(AbstractSerializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = serializers.ListSerializer(child=SummaryArtifactSerializer(help_text="Artifact information for summarization."),
                                           help_text="Map of artifact IDs to bodies.")
    model = serializers.CharField(max_length=512, required=False, help_text="The LLM used for summarization.")
    prompt = serializers.CharField(max_length=512, required=False, help_text="The prompt to use for summarizing artifact.")
