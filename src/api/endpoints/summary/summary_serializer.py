from typing import Dict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer


class SummarySerializer(AbstractSerializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = serializers.ListSerializer(child=serializers.DictField())

    def create(self, validated_data: Dict):
        """
        Creates payload
        :param validated_data:
        :return:
        """
        pass
