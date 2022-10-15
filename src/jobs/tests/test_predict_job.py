import json

import mock
from mock import patch

from api.responses import BaseResponse
from jobs.job_status import Status
from jobs.predict_job import PredictJob
from jobs.trace_args_builder import TraceArgsBuilder
from models.model_generator import ModelGenerator
from test.base_test import BaseTest
from test.config.paths import TEST_OUTPUT_DIR
from test.test_prediction_output import TEST_PREDICTION_RESPONSE_OUTPUT, assert_output_matches_expected


class TestPredictJob(BaseTest):

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_run_full(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        output_file_path = self.get_expected_output_path(test_predict_job.id) + "/" + PredictJob.OUTPUT_FILENAME
        with open(output_file_path, "r") as outfile:
            lines = outfile.readlines()
        json_str = "".join(lines)
        self.output_test_success(json_str)

    @patch("trace.train.trace_trainer.TraceTrainer.perform_prediction")
    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    @patch.object(PredictJob, "_save")
    def test_run_success(self, save_mock: mock.MagicMock, get_model_mock: mock.MagicMock,
                         get_tokenizer_mock: mock.MagicMock,
                         perform_prediction_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        save_mock.side_effect = self.output_test_success
        perform_prediction_mock.return_value = TEST_PREDICTION_RESPONSE_OUTPUT
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        self.assertTrue(perform_prediction_mock.called)

    @patch("trace.train.trace_trainer.TraceTrainer.perform_prediction")
    @patch.object(ModelGenerator, "get_model")
    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(PredictJob, "_save")
    def test_run_failure(self, save_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock,
                         get_model_mock: mock.MagicMock,
                         perform_prediction_mock: mock.MagicMock):
        save_mock.side_effect = self.output_test_failure
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        perform_prediction_mock.return_value = ValueError()
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        self.assertTrue(perform_prediction_mock.called)

    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    def get_test_predict_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        arg_builder = TraceArgsBuilder(**self.get_test_params(include_links=False))
        return PredictJob(arg_builder)

    def output_test_success(self, output: str):
        output_dict = json.loads(output)
        matches, msg = assert_output_matches_expected(output_dict)
        if not matches:
            self.fail(msg)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)

    def output_test_failure(self, output):
        output_dict = json.loads(output)
        self.assertIn(BaseResponse.EXCEPTION, output_dict)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.FAILURE)

    def get_expected_output_path(self, predict_job_id):
        return TEST_OUTPUT_DIR + "/" + str(predict_job_id)
