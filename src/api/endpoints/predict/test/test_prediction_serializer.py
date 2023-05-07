from api.endpoints.predict.prediction_serializer import PredictionSerializer
from api.tests.api_base_test import ApiBaseTest
from api.tests.test_data import TestData


class TestPredictionSerializer(ApiBaseTest):
    """
    Tests that prediction payload can be serialized.
    """

    def test_pos_serialization(self):
        """
        Tests that valid payload is able to be serialized.
        """
        model_name = "thearod5/pl-bert"
        payload = {
            "model": model_name,
            "dataset": TestData.dataset
        }
        serializer = PredictionSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        data = serializer.save()
        self.assertEqual(model_name, data["model"])
        TestData.assert_valid_dataset(self, data["dataset"])
