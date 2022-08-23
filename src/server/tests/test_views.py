from copy import deepcopy

from django.test import TestCase
from django.test import Client
from django.test.client import JSON_CONTENT_TYPE_RE

from server import views
from server.api import Api
from server.job_type import JobType
from test.test_data import TEST_S_ARTS, TEST_T_ARTS, TEST_POS_LINKS
import numpy as np
import json

from test.test_model import get_test_model
from test.test_tokenizer import get_test_tokenizer
import mock
from mock import patch
import json

class TestViews(TestCase):
    TEST_PARAMS = {Api.SOURCES.value: TEST_S_ARTS,
                   Api.TARGETS.value: TEST_T_ARTS,
                   Api.MODEL_PATH.value: "path/to/model",
                   Api.BASE_MODEL.value: "bert_trace_single",
                   "max_seq_length": 100,
                   "pad_to_max_length": True}
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

    @patch("common.models.model_generator")
    def test_run_job(self, model_generator_mock: mock.MagicMock):
        model_generator_mock.get_model = mock.MagicMock(return_value=get_test_model())
        model_generator_mock.get_tokenizer = mock.MagicMock(return_value=get_test_tokenizer())
        test_request = self.get_test_request('/predict/', self.TEST_PARAMS)
        response = views._run_job(test_request, JobType.PREDICT)

    """
     def test_make_job_params_from_request(self):
        args_builder = views._make_job_params_from_request(self.TEST_PARAMS)
        self.assertEquals(args_builder.sources, self.TEST_PARAMS[Api.SOURCES.value])
        self.assertEquals(args_builder.targets, self.TEST_PARAMS[Api.TARGETS.value])
        self.assertEquals(args_builder.model_path, self.TEST_PARAMS[Api.MODEL_PATH.value])
        self.assertEquals(args_builder.base_model, self.TEST_PARAMS[Api.BASE_MODEL.value])
        for setting, value in self.TEST_PARAMS[Api.SETTINGS.value].items():
            self.assertIn(args_builder.kwargs, setting)
            self.assertEqualss(args_builder.kwargs[setting], value)
        self.assertEquals(args_builder.kwargs["prediction_ids_key"], Api.PREDICTION_IDS)

    def test_as_json(self):
        response = views._as_json(self.TEST_PREDICTION_OUTPUT)
    """

    def get_test_request(self, url: str, params: dict):
        c = Client()
        print("PARAMS", params)
        print(type(params))
        body_str = json.dumps(params)
        print("PARAM STR:", body_str)
        request = c.post(url, data=params, content_type="application/json")
        return request
