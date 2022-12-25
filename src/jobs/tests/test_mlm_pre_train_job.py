import os
from unittest import mock
from unittest.mock import patch

from transformers import AutoModelForMaskedLM

from jobs.components.job_args import JobArgs
from jobs.mlm_pre_train_job import MLMPreTrainJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from test.paths.paths import TEST_DATA_DIR


class TestMLMPreTrainJob(BaseJobTest):
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    @patch.object(ModelManager, '_ModelManager__load_model')
    @patch.object(ModelManager, 'get_tokenizer')
    def _test_run_success(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        self.assert_output_on_success(self._load_job_output(job))

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self):
        params = self.get_job_args(include_pre_processing=True, include_base_model=False)
        trainer_args = self.get_trainer_args()
        job_args = JobArgs(**params)
        return MLMPreTrainJob(job_args)
