from django.test import TestCase
import mock
from mock import patch

from common.jobs.job_result_key import JobResultKey
from common.jobs.job_status import Status
from common.models.model_generator import ModelGenerator
from test.config.paths import TEST_OUTPUT_DIR
from test.test_data import TEST_S_ARTS, TEST_POS_LINKS, TEST_T_ARTS
from test.test_model import get_test_model
from test.test_prediction_output import TEST_PREDICTION_OUTPUT
from test.test_tokenizer import get_test_tokenizer
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.jobs.predict_job import PredictJob
from trace.jobs.trace_args_builder import TraceArgsBuilder
import json
import numpy as np


class TestPredictJob(TestCase):
    test_args = {"base_model_name": "bert_trace_single",
                 "model_path": "model",
                 "output_path": TEST_OUTPUT_DIR,
                 "sources": TEST_S_ARTS,
                 "targets": TEST_T_ARTS,
                 "links": TEST_POS_LINKS,
                 "validation_percentage": VALIDATION_PERCENTAGE_DEFAULT}

    TEST_OUTPUT = {"predictions": TEST_PREDICTION_OUTPUT.predictions,
                   "metrics": TEST_PREDICTION_OUTPUT.metrics,
                   "label_ids": TEST_PREDICTION_OUTPUT.label_ids,
                   "ids": [[s_id, t_id] for s_id in TEST_S_ARTS.keys() for t_id in TEST_T_ARTS.keys()]}

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_run_full(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = get_test_model()
        get_tokenizer_mock.return_value = get_test_tokenizer()
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        output_file_path = self.get_expected_output_path(test_predict_job.id) + "/" + PredictJob.OUTPUT_FILENAME
        with open(output_file_path, "r") as outfile:
            lines = outfile.readlines()
        json_str = "".join(lines)
        self.output_test_success(json_str)

    @patch("trace.train.trace_trainer.TraceTrainer.perform_prediction")
    @patch.object(PredictJob, "_save")
    def test_run_success(self, save_mock: mock.MagicMock, perform_prediction_mock: mock.MagicMock):
        save_mock.side_effect = self.output_test_success
        perform_prediction_mock.return_value = self.TEST_OUTPUT
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        self.assertTrue(perform_prediction_mock.called)

    @patch("trace.train.trace_trainer.TraceTrainer.perform_prediction")
    @patch.object(PredictJob, "_save")
    def test_run_failure(self, save_mock: mock.MagicMock, perform_prediction_mock: mock.MagicMock):
        save_mock.side_effect = self.output_test_failure
        perform_prediction_mock.return_value = ValueError()
        test_predict_job = self.get_test_predict_job()
        test_predict_job.run()
        self.assertTrue(perform_prediction_mock.called)

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_get_output_dir_exists(self, exists_mock: mock.MagicMock, makedirs_mock: mock.MagicMock):
        exists_mock.return_value = True
        test_predict_job = self.get_test_predict_job()
        output_dir = test_predict_job._get_output_dir()
        self.assertEquals(output_dir, self.get_expected_output_path(test_predict_job.id))

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_get_output_dir_not_exists(self, exists_mock: mock.MagicMock, makedirs_mock: mock.MagicMock):
        exists_mock.return_value = False
        test_predict_job = self.get_test_predict_job()
        output_dir = test_predict_job._get_output_dir()
        self.assertEquals(output_dir, self.get_expected_output_path(test_predict_job.id))
        self.assertTrue(makedirs_mock.called)

    @patch("os.path.exists")
    def test_get_output_filepath(self, exists_mock: mock.MagicMock):
        exists_mock.return_value = True
        test_predict_job = self.get_test_predict_job()
        output_filepath = test_predict_job._get_output_filepath()
        self.assertEquals(output_filepath, self.get_expected_output_path(test_predict_job.id) + "/" + PredictJob.OUTPUT_FILENAME)

    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    def get_test_predict_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = get_test_model()
        get_tokenizer_mock.return_value = get_test_tokenizer()
        arg_builder = TraceArgsBuilder(**self.test_args)
        return PredictJob(arg_builder)

    def test_output_as_json(self):
        test_predict_job = self.get_test_predict_job()
        test_predict_job.result = self.TEST_OUTPUT
        test_predict_job.status = Status.SUCCESS
        json_str = test_predict_job.get_output_as_json()
        self.assertTrue(isinstance(json_str, str))
        self.output_test_success(json_str)

    def output_test_success(self, output: str):
        output_dict = json.loads(output)
        for key, value in self.TEST_OUTPUT.items():
            self.assertIn(key, output_dict)
            expected_value = value.tolist() if isinstance(value, np.ndarray) else value
            if isinstance(expected_value, list):
                for i, ele in enumerate(output_dict[key]):
                    if isinstance(ele, list):
                        if isinstance(ele[0], float):
                            for j, x in enumerate(ele):
                                self.assertLessEqual(abs(x - expected_value[i][j]), 0.05)
                            continue
                    self.assertEquals(ele, expected_value[i])
        self.assertIn(JobResultKey.STATUS.value, output_dict)
        self.assertEquals(output_dict[JobResultKey.STATUS.value], Status.SUCCESS)

    def output_test_failure(self, output):
        output_dict = json.loads(output)
        self.assertIn(JobResultKey.EXCEPTION.value, output_dict)
        self.assertIn(JobResultKey.STATUS.value, output_dict)
        self.assertEquals(output_dict[JobResultKey.STATUS.value], Status.FAILURE)

    def get_expected_output_path(self, predict_job_id):
        return TEST_OUTPUT_DIR + "/" + str(predict_job_id)
