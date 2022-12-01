from typing import Dict, Type, Union

from rest_enumfield import EnumField
from rest_framework import serializers

from server.serializers.dataset.pre_processing_step_serializer import PreProcessingStepSerializer
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.serializer_utility import SerializerUtility
from tracer.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator

SupportedDatasets = Union[AbstractTraceDatasetCreator, MLMPreTrainDatasetCreator]


class DatasetCreatorSerializer(serializers.Serializer):
    creator = EnumField(choices=SupportedDatasetCreator,
                        help_text="The class used to create dataset.")
    params = serializers.DictField(help_text="The arguments used to construct dataset.",
                                   required=False)

    preProcessingSteps = PreProcessingStepSerializer(help_text="The steps performed on dataset before model access.",
                                                     many=True,
                                                     source="data_cleaning_steps",
                                                     required=False)

    def create(self, validated_data: Dict) -> SupportedDatasets:
        """
        Uses creator to create dataset with params and pre-processing steps.
        :param validated_data: Data describing creator, its parameters, and pre-processing steps.
        :return: AbstractDatasetCreator containing TraceDataset or PreTrainDataset
        """
        kwargs = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        pre_processing_steps = kwargs.get("data_cleaning_steps", None)
        params = kwargs.get("params", {})
        creator_class: Type[SupportedDatasets] = kwargs["creator"].value
        return creator_class(pre_processing_steps=pre_processing_steps, **params)

    def update(self, instance, validated_data):
        SerializerUtility.update_error()

    def to_representation(self, instance: AbstractDatasetCreator):
        return JobFactoryConverter.abstract_dataset_creator_representation(instance)
