import json
from unittest import mock
from unittest.mock import patch

from api.responses.base_response import BaseResponse
from jobs.job_status import Status
from jobs.predict_job import PredictJob
from test.base_test import BaseTest
from test.config.paths import TEST_OUTPUT_DIR
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.model_generator import ModelGenerator


class TestPredictJob(BaseTest):
    TEST_PARAMS = BaseTest.get_test_params(dataset_role=DatasetRole.EVAL, include_trace_params=True, include_links=False)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_run_full(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        output_file_path = test_predict_job.job_output_filepath
        with open(output_file_path, "r") as outfile:
            lines = outfile.readlines()
        json_str = "".join(lines)
        self.output_test_success(json_str)

    @patch("tracer.train.trace_trainer.TraceTrainer.perform_prediction")
    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    @patch.object(PredictJob, "_save")
    def test_run_success(self, save_mock: mock.MagicMock, get_model_mock: mock.MagicMock,
                         get_tokenizer_mock: mock.MagicMock,
                         perform_prediction_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        save_mock.side_effect = self.output_test_success
        perform_prediction_mock.return_value = self.TEST_PREDICTION_RESPONSE_OUTPUT
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        self.assertTrue(perform_prediction_mock.called)

    @patch("tracer.train.trace_trainer.TraceTrainer.perform_prediction")
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
        return PredictJob(**self.TEST_PARAMS)

    def output_test_success(self, output: str):
        output_dict = json.loads(output)
        self.assert_output_matches_expected(output_dict)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)

    def output_test_failure(self, output):
        output_dict = json.loads(output)
        self.assertIn(BaseResponse.EXCEPTION, output_dict)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.FAILURE)

    def get_expected_output_path(self, predict_job_id):
        return TEST_OUTPUT_DIR + "/" + str(predict_job_id)

