from typing import Optional, TypedDict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.serializers.dataset_serializer import DatasetSerializer
from tgen.server.api.api_definition import ApiDefinition


class PredictionPayload(TypedDict):
    """
    Types the payload for the prediction endpoint.
    """
    dataset: ApiDefinition
    model: str
    prompt: Optional[str]


class PredictionSerializer(AbstractSerializer):
    """
    Serializes prediction payload.
    """
    KEY = "definition"
    dataset = DatasetSerializer(help_text="The dataset to predict on.")
    prompt = serializers.CharField(max_length=512, required=False, allow_null=True,
                                   help_text="Custom prompt deciding what tracing means.")
