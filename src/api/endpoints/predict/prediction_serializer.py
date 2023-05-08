from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.serializers.dataset_serializer import DatasetSerializer


class PredictionSerializer(AbstractSerializer):
    """
    Serializes prediction payload.
    """
    KEY = "definition"
    model = serializers.CharField(max_length=512)
    dataset = DatasetSerializer()
    prompt = serializers.CharField(max_length=512, required=False, allow_null=True)
