from api.endpoints.predict.predict_serializer import PredictionSerializer
from api.tests.api_base_test import APIBaseTest
from api.tests.test_data import TestData


class TestPredictionSerializer(APIBaseTest):
    """
    Tests that prediction payload can be serialized.
    """

    def test_pos_serialization(self):
        """
        Tests that valid payload is able to be serialized.
        """
        payload = {
            "dataset": TestData.dataset
        }
        serializer = PredictionSerializer(data=payload)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        data = serializer.save()
        TestData.assert_valid_dataset(self, data["dataset"])
