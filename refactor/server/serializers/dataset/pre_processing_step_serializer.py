from typing import Dict, Type

from rest_enumfield import EnumField
from rest_framework import serializers

from tracer.pre_processing.pre_processing_steps import PreProcessingSteps
from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep
from tracer.util.reflection_util import ParamScope, ReflectionUtil


class PreProcessingStepSerializer(serializers.Serializer):
    step = EnumField(choices=PreProcessingSteps,
                     help_text="The pre-processing step to perform.")
    params = serializers.DictField(help_text="The arguments used to construct step.", required=False)

    def create(self, validated_data: Dict) -> AbstractPreProcessingStep:
        step_class: Type[AbstractPreProcessingStep] = validated_data["step"].value
        params = validated_data["params"] if "params" in validated_data else {}
        return step_class(**params)

    def update(self, instance, validated_data: Dict) -> AbstractPreProcessingStep:
        return ReflectionUtil.set_attributes(instance, validated_data["params"])

    def to_representation(self, instance: AbstractPreProcessingStep):
        return {
            "step": ReflectionUtil.get_enum_key(PreProcessingSteps, instance),
            "params": ReflectionUtil.get_fields(instance, ParamScope.LOCAL)
        }
