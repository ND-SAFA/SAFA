from typing import Dict

from jobs.job_factory import JobFactory
from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer


class TrainingRequestSerializer(PredictionRequestSerializer):
    """
    The serializer for training a model.
    """

    def create(self, validated_data: Dict) -> JobFactory:
        return super().create(validated_data, "train")
