from unittest import mock
from unittest.mock import patch

from api.responses.base_response import BaseResponse
from jobs.job_status import Status
from jobs.train_job import TrainJob
from test.base_test import BaseTest
from test.config.paths import TEST_OUTPUT_DIR
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.model_generator import ModelGenerator
from tracer.train.trace_trainer import TraceTrainer
import json
import numpy as np

class TestTrainJob(BaseTest):
    TEST_OUTPUT = {'global_step': 3, 'training_loss': 0.6927204132080078,
                   'metrics': {'train_runtime': 0.1516, 'train_samples_per_second': 79.13,
                               'train_steps_per_second': 19.782, 'train_loss': 0.6927204132080078, 'epoch': 3.0},
                   'status': 0}
    TEST_PARAMS = BaseTest.get_test_params(dataset_role=DatasetRole.TRAIN, include_trace_params=True, include_links=True)

    @patch.object(TraceTrainer, "save_model")
    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_run_full(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock,
                      save_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        test_train_job = self.get_test_train_job()
        test_train_job.run()
        output_file_path = test_train_job.job_output_filepath
        with open(output_file_path, "r") as outfile:
            lines = outfile.readlines()
        json_str = "".join(lines)
        self.output_test_success(json_str)

    @patch("tracer.train.trace_trainer.TraceTrainer.perform_training")
    @patch.object(ModelGenerator, "get_model")
    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(TrainJob, "_save")
    def test_run_success(self, save_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock,
                         get_model_mock: mock.MagicMock, perform_training_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        save_mock.side_effect = self.output_test_success
        perform_training_mock.return_value = self.TEST_OUTPUT
        test_train_job = self.get_test_train_job()
        test_train_job.run()
        self.assertTrue(perform_training_mock.called)

    @patch("tracer.train.trace_trainer.TraceTrainer.perform_training")
    @patch.object(ModelGenerator, "get_model")
    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(TrainJob, "_save")
    def test_run_failure(self, save_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock,
                         get_model_mock: mock.MagicMock, perform_training_mock: mock.MagicMock):
        save_mock.side_effect = self.output_test_failure
        perform_training_mock.return_value = ValueError()
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        test_train_job = self.get_test_train_job()
        test_train_job.run()
        self.assertTrue(perform_training_mock.called)

    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    def get_test_train_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        return TrainJob(**self.TEST_PARAMS)

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
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)

    def output_test_failure(self, output):
        output_dict = json.loads(output)
        self.assertIn(BaseResponse.EXCEPTION, output_dict)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.FAILURE)

    def get_expected_output_path(self, train_job_id):
        return TEST_OUTPUT_DIR + "/" + str(train_job_id)
