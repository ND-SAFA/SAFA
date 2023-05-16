from typing import Dict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.data.chunkers.supported_chunker import SupportedChunker


class SummaryArtifactSerializer(serializers.Serializer):
    """
    Serializes a summary artifact request.
    """
    content = serializers.CharField(max_length=4112, help_text="The content to summarize.")
    type = serializers.ChoiceField(choices=[(e.name, e.value) for e in SupportedChunker],
                                   help_text="The type of chunker to use for segmenting document.")


class SummarySerializer(AbstractSerializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = serializers.DictField(child=SummaryArtifactSerializer())
    model = serializers.CharField(max_length=512, required=False)
    prompt = serializers.CharField(max_length=512, required=False)

    def create(self, validated_data: Dict):
        """
        Creates payload
        :param validated_data:
        :return:
        """
        data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return data
