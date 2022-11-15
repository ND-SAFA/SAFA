from django.test import TestCase

from server.serializers.prediction_request_serializer import PredictionRequestSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest


class TestPredictionRequestSerializer(TestCase):
    """
    Test that the PredictionRequestSerializer is able to create PredictionRequest from JSON and export PredictionRequest
    as JSON
    """
    serializer_test_data = {
        "baseModel": "NL_BERT",
        "modelPath": "~/desktop/safa/datasets",
        "outputDir": "hello",
        "loadFromStorage": True,
        "sourceLayers": [{"S1": "hello"}],
        "targetLayers": [{"T1": "world"}],
        "settings": {
            "num_train_epochs": 1
        }
    }
    serializer_test = BaseSerializerTest(PredictionRequestSerializer)

    def test_serialization(self):
        prediction_request = self.serializer_test.serialize_data(self, self.serializer_test_data)
        BaseSerializerTest.assert_contains_camel_case_properties(self, prediction_request, self.serializer_test_data)

    def test_deserialization(self):
        self.serializer_test.serialize_deserialize_data(self, self.serializer_test_data)

    def test_update(self):
        new_properties = {"loadFromStorage": False}
        self.serializer_test.serialize_update_data(self, self.serializer_test_data, new_properties)

    def test_invalid_update(self):
        invalid_properties = {"loadFromStorage": 12}
        self.serializer_test.test_invalid_update(self, self.serializer_test_data, invalid_properties)
