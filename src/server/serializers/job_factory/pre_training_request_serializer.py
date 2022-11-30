from typing import Dict

from rest_framework import serializers

from jobs.job_factory import JobFactory
from server.serializers.dataset.pre_processing_step_serializer import PreProcessingStepSerializer
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.job_factory.model_identifier_serializer import ModelIdentifierSerializer
from server.serializers.serializer_utility import SerializerUtility
from tracer.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class PreTrainingRequestSerializer(ModelIdentifierSerializer):
    """
    Serializer for pre-training a model.
    """
    trainingDataDir = serializers.CharField(max_length=200,
                                            source="training_data_dir",
                                            help_text="Path to directory containing pre-training documents.")
    preProcessingSteps = PreProcessingStepSerializer(help_text="The steps performed on dataset before model access.",
                                                     many=True,
                                                     source="pre_processing_steps",
                                                     required=False)
    params = serializers.DictField(help_text="Arguments for passed into hugging face trainer.")

    def create(self, validated_data: Dict) -> JobFactory:
        kwargs = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)

        pre_processing_steps = kwargs.pop("pre_processing_steps", None)
        training_data_dir = kwargs.pop("training_data_dir")

        training_dataset_creator = MLMPreTrainDatasetCreator(orig_data_path=training_data_dir,
                                                             pre_processing_steps=pre_processing_steps)
        trainer_datasets_container = TrainerDatasetsContainer(train=training_dataset_creator)
        return JobFactory(**kwargs, trainer_dataset_container=trainer_datasets_container)

    def to_representation(self, instance: JobFactory) -> Dict:
        representation = {}
        job_factory_representation = JobFactoryConverter.job_factory_representation(instance)
        for field_name, field in self.fields.fields.items():
            if field_name in job_factory_representation:
                representation[field_name] = job_factory_representation[field_name]
        pre_train_dataset_creator: MLMPreTrainDatasetCreator = instance.trainer_dataset_container.get_creator(
            DatasetRole.TRAIN)
        representation["preProcessingSteps"] = [JobFactoryConverter.abstract_pre_processing_step_representation(step)
                                                for step in pre_train_dataset_creator._pre_processor.steps]
        representation["trainingDataDir"] = pre_train_dataset_creator.orig_data_path

        return representation
