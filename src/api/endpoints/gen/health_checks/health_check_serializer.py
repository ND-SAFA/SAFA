from dataclasses import dataclass

from api.constants.api_constants import TEXT_MEDIUM
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.gen.serializers.dataset_serializer import DatasetSerializer
from tgen.common.util.base_object import BaseObject
from tgen.data.readers.definitions.api_definition import ApiDefinition
from rest_framework import serializers


@dataclass
class HealthCheckRequest(BaseObject):
    dataset: ApiDefinition
    query_id: str
    concept_layer_id: str


class HealthCheckSerializer(AbstractSerializer):
    """
    Serializes the request for performing health checks on an artifact.
    """
    dataset = DatasetSerializer(help_text="The dataset used for context and contains the query artifact.")
    query_id = serializers.CharField(max_length=TEXT_MEDIUM, help_text="The id of the query artifact under inspection.")
    concept_layer_id = serializers.CharField(max_length=TEXT_MEDIUM, help_text="The id of layer containing concept artifacts.")

    def create(self, validated_data) -> HealthCheckRequest:
        """
        Serializes Health Check request.
        :param validated_data: The JSON input data.
        :return: Health Check Request.
        """
        dataset_serializer = DatasetSerializer(data=validated_data["dataset"])
        dataset_serializer.is_valid(raise_exception=True)
        dataset = dataset_serializer.save()
        query_id = validated_data["query_id"]
        concept_layer_id = validated_data["concept_layer_id"]
        return HealthCheckRequest(dataset=dataset, query_id=query_id, concept_layer_id=concept_layer_id)
