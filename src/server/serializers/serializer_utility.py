from typing import Dict, List, OrderedDict, Tuple

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from data.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.trainer_datasets_container import TrainerDatasetsContainer
from data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep


class SerializerUtility:
    """
    Helper class for generalizing serializer logic and job factory construction.
    """

    @staticmethod
    def serialize_trainer_dataset_container(kwargs: Dict, dataset_params: List[Tuple[str, str]],
                                            export_param: str = "trainer_dataset_container", **addition_kwargs):
        """
        Reads dataset from kwargs and wraps it in a trainer dataset container.
        :param kwargs: The kwargs to extract dataset from.
        :param dataset_params: List of parameter conversions from validated data to trainer dataset container.
        :param export_param: The name of the parameter to export trainer dataset container to in kwargs.
        :return: None
        """
        container_kwargs = {}
        for dataset_param, container_param in dataset_params:
            dataset_creator: AbstractDatasetCreator = kwargs.pop(dataset_param)
            container_kwargs[container_param] = dataset_creator
        trainer_datasets_container = TrainerDatasetsContainer(**container_kwargs, **addition_kwargs)
        kwargs[export_param] = trainer_datasets_container

    @staticmethod
    def update_error():
        """
        Throws a not implemented error with a consistent message.
        :return: None
        """
        raise NotImplementedError("Update has not implemented for serializers. Please create new serialier.")

    @staticmethod
    def assert_no_unknown_fields(initial_data: Dict, fields: OrderedDict):
        """
        Asserts that all fields in initial data have a corresponding field.
        :param initial_data: The data used to initialize a serializer.
        :param fields: The fields of the serializer.
        :return: None
        """
        if initial_data:
            unknown_keys = set(initial_data.keys()) - set(fields.keys())
            if unknown_keys:
                raise ValidationError("Got unknown fields: {}".format(unknown_keys))

    @staticmethod
    def create_children_serializers(validated_data: Dict, fields: OrderedDict) -> Dict:
        """
        Creates each field in serializer of type serializer.
        :param validated_data: The validated request data.
        :param fields: The fields of the serializer.
        :return: Dictionary containing created field values.
        """
        kwargs = {}
        for field in fields.values():
            field_name = field.source
            if field_name not in validated_data:
                continue
            is_serializer = isinstance(field, serializers.Serializer)
            has_child_serializer = hasattr(field, "child") and isinstance(field.child, serializers.Serializer)
            if is_serializer or has_child_serializer:
                kwargs[field_name] = field.create(validated_data[field_name])
            else:
                kwargs[field_name] = validated_data[field_name]
        return kwargs

    @staticmethod
    def to_camel_case(word: str):
        words = word.lower().split("_")
        words = words[:1] + [w.title() for w in words[1:]]
        return "".join(words)

    @staticmethod
    def to_snake_case(word: str):
        """
        Wrapper for performing snake case conversion to single word.
        :param word: The string to convert.
        :return: word in snake_case.
        """
        return "_".join(list(map(lambda w: w.lower(), SeparateJoinedWordsStep.separate_camel_case_word(word))))
