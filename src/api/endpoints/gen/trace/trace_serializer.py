from typing import TypedDict

from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.gen.serializers.dataset_serializer import DatasetSerializer
from tgen.data.readers.definitions.api_definition import ApiDefinition


class TraceRequest(TypedDict):
    """
    Types the payload for the prediction endpoint.
    """
    dataset: ApiDefinition


class PredictionSerializer(AbstractSerializer):
    """
    Serializes prediction payload.
    """
    KEY = "definition"
    dataset = DatasetSerializer(help_text="The dataset to predict on.")

    def create(self, validated_data):
        """
        Serializes the input data to a trace prediction endpoint.
        :param validated_data: The validated data.
        :return: Serialized dataset.
        """
        dataset_data = validated_data.pop("dataset")
        dataset_serializer = DatasetSerializer(data=dataset_data)
        dataset_serializer.is_valid(raise_exception=True)
        dataset = dataset_serializer.save()
        return {
            "dataset": dataset, **validated_data
        }
