from dataclasses import dataclass
from typing import List, Tuple

from rest_framework import serializers

from server.serializers.base_serializer import BaseSerializer
from server.serializers.prediction_request_serializer import PredictionRequest, PredictionRequestSerializer


@dataclass
class TrainingRequest(PredictionRequest):
    links: List[Tuple[str, str]]


class TrainingRequestSerializer(PredictionRequestSerializer, BaseSerializer[PredictionRequest]):
    links = serializers.ListField(child=serializers.ListField(child=serializers.CharField()),
                                  help_text="List of true links.")

    def get_app_entity_class(self):
        return TrainingRequest
