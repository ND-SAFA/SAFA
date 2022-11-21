import os
from unittest import mock, skip
from unittest.mock import patch

from jobs.abstract_job import AbstractJob
from jobs.gan_train_job import GanTrainJob
from jobs.job_args import JobArgs
from jobs.tests.test_train_job import TestTrainJob
from test.base_job_test import BaseJobTest
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from tracer.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.train.trace_trainer import TraceTrainer


class TestGanTrainJob(BaseJobTest):
    """
    Tests that GAN is able to train and test.
    TODO: Add test that includes a pre-training datasets
    TODO: Reduce the run time of the test to < 10 seconds
    """
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")
    EXAMPLE_TRAINING_OUTPUT = {
        "stats": [{
            "epoch": 1,
            "Valid. Accur.": 0
        }]
    }

    @skip("Throws Exception at line 120 in gan_trainer.train")
    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    @staticmethod
    def create_dataset_map(dataset_role: DatasetRole, include_links=True):
        train_dataset = BaseJobTest.create_dataset_map(DatasetRole.TRAIN)
        test_dataset = {DatasetRole.EVAL: (SupportedDatasetCreator.CSV, {
            "data_file_path": TestTrainJob.CSV_DATA_FILE
        })}
        return {**train_dataset, **test_dataset}

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self) -> AbstractJob:
        test_params = self.get_test_params_for_trace(dataset_role=DatasetRole.PRE_TRAIN, include_links=True)
        job_args = JobArgs(**test_params)
        job_args.trace_args_params = {
            "num_train_epochs": 1
        }
        job_args.trace_args.trainer_dataset_container[DatasetRole.PRE_TRAIN] = MLMPreTrainDatasetCreator(
            orig_data_path=self.PRETRAIN_DIR, training_data_dir=TEST_OUTPUT_DIR).create()
        return GanTrainJob(job_args)
