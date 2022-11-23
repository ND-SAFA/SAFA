from typing import Dict

from jobs.job_factory import JobFactory
from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer


class TrainingRequestSerializer(PredictionRequestSerializer):

    def create(self, validated_data: Dict) -> JobFactory:
        super().create(validated_data, "train")
