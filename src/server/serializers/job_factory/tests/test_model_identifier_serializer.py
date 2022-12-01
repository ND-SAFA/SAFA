from server.serializers.job_factory.model_identifier_serializer import ModelIdentifierSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from test.base_test import BaseTest
import unittest

@unittest.skip("Needs Fixed")
class TestModelIdentifierSerializer(BaseTest):
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

        def run_update():
            self.serializer_test.test_no_update(self, self.serializer_test_data, new_properties)

        self.assertRaises(NotImplementedError, run_update)
