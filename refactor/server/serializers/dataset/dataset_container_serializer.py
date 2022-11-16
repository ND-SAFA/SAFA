from typing import Dict

from rest_framework import serializers

from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class TrainerDatasetsContainerSerializer(serializers.Serializer):
    preTrain = DatasetCreatorSerializer(help_text="The instructions for creating pre-training dataset.",
                                        required=False,
                                        source="pre_train")
    train = DatasetCreatorSerializer(help_text="The instructions for creating training dataset.",
                                     required=False)
    val = DatasetCreatorSerializer(help_text="The instructions for creating validation dataset.",
                                   required=False)
    eval = DatasetCreatorSerializer(help_text="The instructions for creating testing dataset.",
                                    required=False)

    def update(self, instance, validated_data):
        raise NotImplementedError("Updating is not supported. Please create new object.")

    def create(self, validated_data: Dict):
        kwargs = {}
        for dataset_key in validated_data:
            dataset_data = validated_data[dataset_key]
            serializer = DatasetCreatorSerializer(data=dataset_data)
            kwargs[dataset_key] = serializer.create(dataset_data)
        return TrainerDatasetsContainer(**kwargs)
