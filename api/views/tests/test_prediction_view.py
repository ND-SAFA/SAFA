from tests.api_base_test import ApiBaseTest
from tests.test_data import TestData


class TestPredictionView(ApiBaseTest):
    """
    Tests trace link prediction endpoint.
    """

    def test_pos_generate(self):
        data = {
            "model": "hf-internal-testing/tiny-random-bert",
            "dataset": TestData.dataset
        }
        res = self.request("/predict/", data=data)
