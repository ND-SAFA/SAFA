from typing import Dict

from rest_framework import serializers

from jobs.job_factory import JobFactory
from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from server.serializers.job_factory.model_identifier_serializer import ModelIdentifierSerializer
from server.serializers.serializer_utility import SerializerUtility
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class PredictionRequestSerializer(ModelIdentifierSerializer):
    data = DatasetCreatorSerializer(help_text="The instructions for creating training/prediction dataset.",
                                    required=True)
    settings = serializers.DictField(help_text="Custom training arguments.", required=False)

    def create(self, validated_data: Dict, dataset_param_key="eval") -> JobFactory:
        kwargs: Dict = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        dataset = kwargs.pop("data").create()
        kwargs.update(kwargs.pop("settings"))  # put settings in main kwargs
        container_kwargs = {dataset_param_key: dataset}
        trainer_datasets_container = TrainerDatasetsContainer(**container_kwargs)
        kwargs["trainer_dataset_container"] = trainer_datasets_container
        return JobFactory(**kwargs)
