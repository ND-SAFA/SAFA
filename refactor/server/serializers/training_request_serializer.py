from rest_framework import serializers

from server.serializers.prediction_request_serializer import PredictionRequestSerializer


class TrainingRequestSerializer(PredictionRequestSerializer):
    links = serializers.ListField(child=serializers.ListField(child=serializers.CharField()),
                                  help_text="List of true links.")
