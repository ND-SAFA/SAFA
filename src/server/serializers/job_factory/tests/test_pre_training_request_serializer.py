from server.serializers.job_factory.pre_training_request_serializer import PreTrainingRequestSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from test.base_test import BaseTest
from util.reflection_util import ReflectionUtil
import unittest

@unittest.skip("Needs Fixed")
class TestPreTrainingRequestSerializer(BaseTest):
    """
    Test that the PredictionRequestSerializer is able to create PredictionRequest from JSON and export PredictionRequest
    as JSON
    """
    serializer_test_data = {
        "baseModel": "NL_BERT",
        "modelPath": "~/desktop/safa/datasets",
        "outputDir": "hello",
        "saveJobOutput": False,
        "trainingDataDir": "src/test/data/pre_train",
        "preProcessingSteps": [
            {
                "step": "SEPARATE_JOINED_WORDS",
                "params": {
                    "deliminators": ["*"]
                }
            }
        ],
        "params": {
            "blockSize": 120,
            "mlmProbability": .5,
        }
    }

    serializer_test = BaseSerializerTest(PreTrainingRequestSerializer)

    def test_serialization(self):
        # Verify job factory properties
        expected_job_factory_fields = ["baseModel", "modelPath", "outputDir", "saveJobOutput"]
        expected_job_factory_properties = ReflectionUtil.copy_fields(self.serializer_test_data,
                                                                     expected_job_factory_fields)

        training_request = self.serializer_test.serialize_data(self, self.serializer_test_data)
        BaseSerializerTest.assert_contains_camel_case_properties(self, training_request,
                                                                 expected_job_factory_properties)

        # Test additional properties
        additional_properties = training_request.additional_job_params
        expected_additional_fields = ["trainingDataDir", "blockSize", "mlmProbability"]
        expected_additional_properties = ReflectionUtil.copy_fields(self.serializer_test_data,
                                                                    expected_additional_fields)
        BaseSerializerTest.assert_contains_camel_case_properties(self, additional_properties,
                                                                 expected_additional_properties)

    def test_deserialization(self):
        self.serializer_test.serialize_deserialize_data(self, self.serializer_test_data)

    def test_update(self):
        new_properties = {"preProcessingSteps": [{"step": "REMOVE_UNWANTED_CHARS"}, {"step": "SEPARATE_JOINED_WORDS"}]}

        def run_update():
            self.serializer_test.test_no_update(self, self.serializer_test_data, new_properties)

        self.assertRaises(NotImplementedError, run_update)

    def test_invalid_update(self):
        invalid_properties = {"params": []}
        self.serializer_test.test_invalid_update(self, self.serializer_test_data, invalid_properties,
                                                 expected_phrase="list")
