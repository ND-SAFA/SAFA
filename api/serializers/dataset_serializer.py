from rest_framework import serializers

from serializers.serializer_utility import SerializerUtility
from tgen.src.server.api.api_definition import ApiDefinition


class DatasetSerializer(serializers.Serializer):
    """
    Serializes datasets for trace link prediction.
    """
    source_layers = serializers.ListField(child=serializers.DictField(),
                                          help_text="List of source artifacts layers.",
                                          required=True)
    target_layers = serializers.ListField(child=serializers.DictField(),
                                          help_text="List of target artifacts layers.",
                                          required=True)

    def update(self, **kwargs):
        """
        Throws error, not implemented.
        :param kwargs: Ignored parameters.
        :return: None, error is thrown.
        """
        SerializerUtility.update_error()

    def create(self, validated_data) -> ApiDefinition:
        """
        Validates dataset payload.
        :param validated_data: The data validated by django.
        :return:
        """
        SerializerUtility.assert_no_unknown_fields(validated_data, self.fields.fields)
        SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        n_source_layers = len(validated_data["source_layers"])
        n_target_layers = len(validated_data["target_layers"])
        assert n_source_layers == n_target_layers, f"Expected number of source and target layers to match: {n_source_layers} != {n_target_layers}"
        return ApiDefinition(source_layers=validated_data["source_layers"], target_layers=validated_data["target_layers"],
                             true_links=[])
