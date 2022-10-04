import json
from typing import Dict

import mock
from django.test import Client
from mock import patch

from common.api.responses import BaseResponse
from common.jobs.job_status import Status
from common.models.model_generator import ModelGenerator
from test.base_test import BaseTest
from test.config.paths import TEST_OUTPUT_DIR


class TestViews(BaseTest):

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch('common.models.model_generator.ModelGenerator.get_tokenizer')
    def test_create_model(self, get_tokenizer_mock, load_model_mock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        response_dict = self.make_test_request('/model/create/',
                                               self.get_test_params(include_artifacts=False, as_api=True))
        self.assertIn(BaseResponse.MODEL_PATH, response_dict)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch('common.models.model_generator.ModelGenerator.get_tokenizer')
    def test_train(self, get_tokenizer_mock, load_model_mock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        response_dict = self.make_test_request('/train/', self.get_test_params(as_api=True))
        self.assertIn(BaseResponse.JOB_ID, response_dict)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_predict(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        response_dict = self.make_test_request('/predict/', self.get_test_params(include_links=False, as_api=True))
        self.assertIn(BaseResponse.JOB_ID, response_dict)

    def test_delete_model(self):
        response_dict = self.make_test_request('/model/delete/', {BaseResponse.MODEL_PATH: TEST_OUTPUT_DIR})
        self.assertIn(BaseResponse.STATUS, response_dict)
        self.assertEqual(response_dict[BaseResponse.STATUS], Status.SUCCESS.value)

    def test_bad_request(self):
        bad_params = self.get_test_params(as_api=True)
        bad_params["settings"] = {"unknown_arg": 10}
        response_dict = self.make_test_request('/train/', bad_params)
        self.assertIn("settings", response_dict)

    def make_test_request(self, url: str, params: dict) -> Dict:
        c = Client()
        response = c.post(url, data=params, content_type="application/json")
        return json.loads(response.content)
