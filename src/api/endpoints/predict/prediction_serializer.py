from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.serializers.dataset_serializer import DatasetSerializer


class PredictionSerializer(AbstractSerializer):
    """
    Serializes prediction payload.
    """
    KEY = "definition"
    model = serializers.CharField(max_length=512, help_text="The LLM used for prediction.")
    dataset = DatasetSerializer(help_text="The dataset to predict on.")
    prompt = serializers.CharField(max_length=512, required=False, allow_null=True,
                                   help_text="Custom prompt deciding what tracing means.")
