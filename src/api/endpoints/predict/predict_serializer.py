from typing import TypedDict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.serializers.dataset_serializer import DatasetSerializer
from tgen.server.api.api_definition import ApiDefinition


class PredictionPayload(TypedDict):
    """
    Types the payload for the prediction endpoint.
    """
    dataset: ApiDefinition
    summary: str


class PredictionSerializer(AbstractSerializer):
    """
    Serializes prediction payload.
    """
    KEY = "definition"
    dataset = DatasetSerializer(help_text="The dataset to predict on.")
    prompt = serializers.CharField(max_length=512, required=False, allow_null=True,
                                   help_text="Custom prompt deciding what tracing means.")
    summary = serializers.CharField(max_length=1000000,
                                    required=False,
                                    allow_null=True,
                                    help_text="The project summary to include in tracing projects.")

    def create(self, validated_data):
        dataset_data = validated_data.pop("dataset")
        dataset_serializer = DatasetSerializer(data=dataset_data)
        dataset_serializer.is_valid(raise_exception=True)
        dataset = dataset_serializer.save()
        return {
            "dataset": dataset, **validated_data
        }
