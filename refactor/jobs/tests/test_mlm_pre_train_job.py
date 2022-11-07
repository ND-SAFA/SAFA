import os
from unittest import mock
from unittest.mock import patch

from transformers import AutoModelForMaskedLM

from jobs.job_args import JobArgs
from jobs.mlm_pre_train_job import MLMPreTrainJob
from test.base_job_test import BaseJobTest
from test.config.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from tracer.dataset.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.models.model_generator import ModelGenerator


class TestMLMPreTrainJob(BaseJobTest):
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def _test_run_success(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        self.assert_output_on_success(self._load_job_output(job))

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self):
        params = self.get_test_params(include_pre_processing=True, include_base_model=False)
        params["base_model"] = SupportedBaseModel.AUTO_MODEL
        params["datasets_map"] = {
            DatasetRole.PRE_TRAIN: MLMPreTrainDatasetCreator(self.PRETRAIN_DIR)
        }
        job_args = JobArgs(**params)
        return MLMPreTrainJob(job_args,
                              orig_data_path=self.PRETRAIN_DIR,
                              training_data_dir=TEST_OUTPUT_DIR)
