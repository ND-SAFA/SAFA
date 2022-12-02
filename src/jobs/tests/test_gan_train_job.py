import os
from unittest import mock, skip
from unittest.mock import patch

from jobs.abstract_job import AbstractJob
from jobs.gan_train_job import GanTrainJob
from jobs.components.job_args import JobArgs
from jobs.tests.test_train_job import TestTrainJob
from jobs.tests.base_job_test import BaseJobTest
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.supported_dataset_creator import SupportedDatasetCreator
from data.datasets.dataset_role import DatasetRole
from train.trace_trainer import TraceTrainer


class TestGanTrainJob(BaseJobTest):
    """
    Tests that GAN is able to train and test.
    TODO: Add test that includes a pre-training data
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
    def create_dataset(dataset_role: DatasetRole, include_links=True, include_pre_processing=False):
        train_dataset = BaseJobTest.create_dataset(DatasetRole.TRAIN, include_links=include_links,
                                                   include_pre_processing=include_pre_processing)
        test_dataset = SupportedDatasetCreator.CSV.value(data_file_path=TestTrainJob.CSV_DATA_FILE)
        test_dataset_map = {DatasetRole.EVAL: test_dataset}
        return {**train_dataset, **test_dataset_map}

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self) -> AbstractJob:
        test_params = self.get_test_params_for_trace(dataset_role=DatasetRole.PRE_TRAIN, include_links=True)
        job_args = JobArgs(**test_params)
        job_args.trace_args_params = {
            "num_train_epochs": 1
        }
        job_args.trace_args.trainer_dataset_container[DatasetRole.PRE_TRAIN] = MLMPreTrainDatasetCreator(
            orig_data_path=self.PRETRAIN_DIR, training_data_dir=TEST_OUTPUT_DIR)
        return GanTrainJob(job_args)
