import json

import mock
from mock import patch

from common.api.responses import BaseResponse
from common.jobs.job_status import Status
from common.models.model_generator import ModelGenerator
from test.base_test import BaseTest
from trace.jobs.create_model_job import CreateModelJob
from trace.jobs.trace_args_builder import TraceArgsBuilder


class TestModelJob(BaseTest):
    TEST_PARAMS = BaseTest.get_test_params(include_artifacts=False)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_run_full(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        test_model_job = self.get_test_model_job()
        test_model_job.run()
        self.output_test_success(test_model_job.result)

    @patch.object(ModelGenerator, "get_model")
    @patch.object(ModelGenerator, "get_tokenizer")
    def test_run_failure(self, get_tokenizer_mock: mock.MagicMock, get_model_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        get_model_mock.return_value = ValueError()
        test_model_job = self.get_test_model_job()
        test_model_job.run()
        self.output_test_failure(test_model_job.result)

    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    def get_test_model_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        arg_builder = TraceArgsBuilder(**self.TEST_PARAMS)
        return CreateModelJob(arg_builder)

    def output_test_success(self, output_dict: dict):
        self.assertIn(BaseResponse.MODEL_PATH, output_dict)
        self.assertEqual(output_dict[BaseResponse.MODEL_PATH], self.TEST_PARAMS["output_dir"])
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)

    def output_test_failure(self, output_dict: dict):
        self.assertIn(BaseResponse.EXCEPTION, output_dict)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.FAILURE)
