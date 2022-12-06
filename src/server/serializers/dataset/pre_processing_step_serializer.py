from typing import Dict, Type

from rest_enumfield import EnumField
from rest_framework import serializers

from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.processing.cleaning.data_cleaning_steps import DataCleaningSteps
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.serializer_utility import SerializerUtility


class DataCleaningStepSerializer(serializers.Serializer):
    step = EnumField(choices=DataCleaningSteps,
                     help_text="The pre-processing step to perform.")
    params = serializers.DictField(help_text="The arguments used to construct step.", required=False)

    def create(self, validated_data: Dict) -> AbstractDataProcessingStep:
        step_class: Type[AbstractDataProcessingStep] = validated_data["step"].value
        params = validated_data["params"] if "params" in validated_data else {}
        return step_class(**params)

    def update(self, instance, validated_data: Dict) -> AbstractDataProcessingStep:
        return SerializerUtility.update_error()

    def to_representation(self, instance: AbstractDataProcessingStep):
        return JobFactoryConverter.abstract_data_cleaning_step_representation(instance)
