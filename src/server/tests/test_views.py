from copy import deepcopy
from typing import Dict

from django.test import TestCase
from django.test import Client
from django.http.response import JsonResponse
from common.models.model_generator import ModelGenerator
from server.api import Api
from test.config.paths import TEST_OUTPUT_DIR
from test.test_data import TEST_S_ARTS, TEST_T_ARTS, TEST_POS_LINKS
import numpy as np
import json
from test.test_model import get_test_model
from test.test_tokenizer import get_test_tokenizer
import mock
from mock import patch


class TestViews(TestCase):
    TEST_PARAMS = {Api.SOURCES.value: TEST_S_ARTS,
                   Api.TARGETS.value: TEST_T_ARTS,
                   Api.MODEL_PATH.value: "path/to/model",
                   Api.BASE_MODEL.value: "bert_trace_single",
                   Api.OUTPUT_PATH.value: TEST_OUTPUT_DIR,
                   "max_seq_length": 100,
                   "pad_to_max_length": True,
                   "should_save": False}
    TEST_METRIC_RESULTS = {'test_loss': 0.6929082870483398}
    TEST_PREDICTIONS = np.array([[0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124]])
    TEST_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
    TEST_PREDICTION_OUTPUT = {"predictions": TEST_PREDICTIONS,
                              "label_ids": TEST_LABEL_IDS,
                              "metrics": TEST_METRIC_RESULTS}

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_fine_tune(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        fine_tune_params = deepcopy(self.TEST_PARAMS)
        fine_tune_params[Api.LINKS.value] = TEST_POS_LINKS
        load_model_mock.return_value = get_test_model()
        get_tokenizer_mock.return_value = get_test_tokenizer()
        response_dict = self.make_test_request('/fine-tune/', fine_tune_params)
        self.assertIn('training_loss', response_dict)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_predict(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = get_test_model()
        get_tokenizer_mock.return_value = get_test_tokenizer()
        response_dict = self.make_test_request('/predict/', self.TEST_PARAMS)
        self.assertIn(Api.PREDICTIONS.value, response_dict)
        self.assertIn(Api.PREDICTION_IDS.value, response_dict)
        self.assertEqual(len(response_dict[Api.PREDICTIONS.value]), len(response_dict[Api.PREDICTION_IDS.value]))

    def make_test_request(self, url: str, params: dict) -> Dict:
        c = Client()
        response = c.post(url, data=params, content_type="application/json")
        return json.loads(response.content)
