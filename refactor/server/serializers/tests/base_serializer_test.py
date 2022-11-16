from enum import Enum
from typing import Any, Dict, Generic, Type, TypeVar
from unittest import TestCase, skip

from jobs.job_factory import JobFactory
from server.serializers.base_serializer import BaseSerializer
from tracer.pre_processing.separate_joined_words_step import SeparateJoinedWordsStep

AppEntity = TypeVar('AppEntity')


class BaseSerializerTest(Generic[AppEntity]):

    def __init__(self, serializer: Type[BaseSerializer[AppEntity]]):
        """
        Provides default tests for testing serialization, deserialization, and update methods of rest_framework Serializer.
        """
        self.serializer = serializer

    @skip("Skipping until Alberto fixes")
    def serialize_data(self, test_case: TestCase, data: Dict, is_valid_value=True) -> AppEntity:
        """
        Serializes the test data into entity and performs validation checks.
        :param test_case: The test case used to assert the validity of serializer.
        :param data: The dictionary used to create object from serializer.
        :param is_valid_value: The expected state of the serializer's is_valid flag.
        :return: Entity created and serializers used
        """
        serializer = self.serializer(data=data)
        is_valid = serializer.is_valid()
        test_case.assertEqual(is_valid_value, is_valid, msg=serializer.errors)
        if is_valid_value:
            test_case.assertEqual(0, len(serializer.errors))
        return serializer.save()

    def serialize_deserialize_data(self, test_case: TestCase, data: Dict):
        """
        Test that given a Entity, the serializer is able to convert it back to json properly.
        :param test_case: The test used to make assertions.
        :param data: The map of values to serialize into entity.
        """
        entity_created = self.serialize_data(test_case, data)
        deserialized_data = self.serializer(entity_created).data
        for key, value in deserialized_data.items():
            test_case.assertIn(key, data.keys())
            test_case.assertEqual(data[key], value)

    def serialize_update_data(self, test_case: TestCase, data: Dict, new_properties: Dict):
        """
        Test that PredictionRequest can be updated with new load_from_storage property.
        :param test_case: The test used to make assertions.
        :param data: The map of values to serialize into entity.
        :param new_properties: The map of values to update entity with (camel case converted to snake case).
        """
        entity_created = self.serialize_data(test_case, data)
        update_serializer = self.serializer(entity_created,
                                            data=new_properties,
                                            partial=True)
        is_valid = update_serializer.is_valid()
        updated_model_identifier = update_serializer.save()

        test_case.assertTrue(is_valid)
        test_case.assertEqual(0, len(update_serializer.errors))
        self.assert_contains_camel_case_properties(test_case, updated_model_identifier, new_properties)

    def test_invalid_update(self, test_case: TestCase, data: Dict, invalid_properties: Dict,
                            expected_phrase: str = "valid"):
        """
        Serializes data and performs update with invalid properties asserting that error is caught.
        :param test_case: The test used to make assertions.
        :param data: The map of values to serialize into entity.
        :param invalid_properties: The map of property names to invalid values to cause errors.
        :param expected_phrase: The phrased expected to be in error message.
        """
        entity_created = self.serialize_data(test_case, data)
        update_serializer = self.serializer(entity_created, data=invalid_properties, partial=True)

        is_valid = update_serializer.is_valid()
        errors = update_serializer.errors
        test_case.assertFalse(is_valid)
        for key, value in invalid_properties.items():
            test_case.assertIn(key, errors)
            test_case.assertIn(expected_phrase, errors[key][0].title().lower())

    @staticmethod
    def assert_contains_camel_case_properties(test_case: TestCase, instance: JobFactory, camel_case_properties: Dict):
        """
        Verifies that instance contains properties (in camel case) with expected values.
        :param test_case: The test used to assert the validity of the properties.
        :param instance: The object whose properties are verified.
        :param camel_case_properties: Dictionary of property names (in camel case) and expected values.
        :return: None, error thrown if there is missing properties or the values are not as expected.
        """
        for key, new_value in camel_case_properties.items():
            object_key = BaseSerializerTest.to_snake_case(key)
            object_value = getattr(instance, object_key)
            object_value = BaseSerializerTest.to_repr(object_value)
            test_case.assertEqual(new_value, object_value)

    @staticmethod
    def to_repr(object_value: Any):
        if isinstance(object_value, Enum):
            return object_value.name
        if isinstance(object_value, list):
            return list(map(BaseSerializerTest.to_repr, object_value))
        return object_value

    @staticmethod
    def to_snake_case(word: str):
        """
        Wrapper for performing snake case conversion to single word.
        :param word: The string to convert.
        :return: word in snake_case.
        """
        return "_".join(list(map(lambda w: w.lower(), SeparateJoinedWordsStep._separate_camel_case_word(word))))
