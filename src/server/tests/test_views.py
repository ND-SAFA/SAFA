import json
from copy import deepcopy
from typing import Dict

import mock
from django.test import Client, TestCase
from mock import patch

from common.api.prediction_request import PredictionRequest
from common.models.model_generator import ModelGenerator
from test.config.paths import TEST_OUTPUT_DIR
from test.test_data import TEST_POS_LINKS, TEST_S_ARTS, TEST_T_ARTS
from test.test_model import get_test_model
from test.test_tokenizer import get_test_tokenizer


class TestViews(TestCase):
    TEST_PARAMS = {PredictionRequest.SOURCES.value: TEST_S_ARTS,
                   PredictionRequest.TARGETS.value: TEST_T_ARTS,
                   PredictionRequest.MODEL_PATH.value: "path/to/model",
                   PredictionRequest.BASE_MODEL.value: "bert_trace_single",
                   PredictionRequest.OUTPUT_PATH.value: TEST_OUTPUT_DIR,
                   "max_seq_length": 100,
                   "pad_to_max_length": True,
                   "should_save": False}

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_fine_tune(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        fine_tune_params = deepcopy(self.TEST_PARAMS)
        fine_tune_params[PredictionRequest.LINKS.value] = TEST_POS_LINKS
        load_model_mock.return_value = get_test_model()
        get_tokenizer_mock.return_value = get_test_tokenizer()
        response_dict = self.make_test_request('/fine-tune/', fine_tune_params)
        self.assertIn(PredictionRequest.OUTPUT_PATH.value, response_dict)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_predict(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = get_test_model()
        get_tokenizer_mock.return_value = get_test_tokenizer()
        response_dict = self.make_test_request('/predict/', self.TEST_PARAMS)
        self.assertIn(PredictionRequest.OUTPUT_PATH.value, response_dict)

    def make_test_request(self, url: str, params: dict) -> Dict:
        c = Client()
        response = c.post(url, data=params, content_type="application/json")
        return json.loads(response.content)
