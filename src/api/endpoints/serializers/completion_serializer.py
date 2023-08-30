from typing import Dict, TypedDict

from rest_framework import serializers

from api.constants.api_constants import LONG_TEXT
from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.variables.variable import Variable


class CompletionPayload(TypedDict):
    """
    Types the completion payload.
    """
    model: str
    prompt: str


class CompletionSerializer(AbstractSerializer):
    """
    Serialized the generation payload
    """
    prompt = serializers.CharField(max_length=LONG_TEXT, trim_whitespace=False, help_text="Prompt for LLM to answer.")

    def create(self, validated_data: Dict) -> Dict[str, Variable]:
        """
        Creates experiment instructions by converting Dict of primitives into
        one of variables.
        :param validated_data: Dictionary composed of primitive values.
        :return: Mapping between keys and variables.
        """
        data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return data
