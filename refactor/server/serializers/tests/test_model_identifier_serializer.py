from django.test import TestCase

from server.serializers.model_identifier_serializer import ModelIdentifierSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest


class TestModelIdentifierSerializer(TestCase):
    """
    Test that the ModelIdentifierSerializers is able to create ModelIdentifier from JSON and export ModelIdentifiers
    as JSON
    """
    serializer_test_data = {
        "baseModel": "NL_BERT",
        "modelPath": "~/desktop/safa/datasets",
        "outputDir": "hello",
        "saveJobOutput": True
    }
    serializer_test = BaseSerializerTest(ModelIdentifierSerializer)

    def test_serialization(self):
        model_identifier = self.serializer_test.serialize_data(self, self.serializer_test_data)
        BaseSerializerTest.assert_contains_camel_case_properties(self, model_identifier, self.serializer_test_data)

    def test_deserialization(self):
        self.serializer_test.serialize_deserialize_data(self, self.serializer_test_data)

    def test_update(self):
        new_properties = {"baseModel": "PL_BERT"}
        self.serializer_test.serialize_update_data(self, self.serializer_test_data, new_properties)

    def test_invalid_update(self):
        invalid_properties = {"baseModel": "test"}
        self.serializer_test.test_invalid_update(self, self.serializer_test_data, invalid_properties)
