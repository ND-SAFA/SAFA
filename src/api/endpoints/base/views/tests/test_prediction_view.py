from api.tests.api_base_test import APIBaseTest
from api.tests.test_data import TestData


class TestPredictionView(APIBaseTest):
    """
    Tests trace link prediction endpoint.
    """

    def test_pos_generate(self):
        data = {
            "model": "hf-internal-testing/tiny-random-bert",
            "dataset": TestData.dataset
        }
        res = self.request("/predict/", data=data)
        print(res)
