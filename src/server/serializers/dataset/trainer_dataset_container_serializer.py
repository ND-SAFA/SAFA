from typing import Dict

from rest_framework import serializers

from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from server.serializers.serializer_utility import SerializerUtility
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
    params = serializers.DictField(help_text="Initialization params for Trainer Dataset Container",
                                   required=True)

    def create(self, validated_data: Dict):
        """
        Creates TrainerDatasetContainer for each defined dataset.
        :param validated_data: The validated request data defining datasets.
        :return: TrainerDatasetsContainer with dataset creators.
        """
        kwargs = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        if "params" in validated_data:
            kwargs.update(validated_data["params"])
        return TrainerDatasetsContainer(**kwargs)

    def update(self, instance, validated_data):
        SerializerUtility.update_error()
