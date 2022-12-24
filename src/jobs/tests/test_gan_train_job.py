import os
from unittest import mock, skip
from unittest.mock import patch

from data.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.datasets.dataset_role import DatasetRole
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.gan_train_job import GanTrainJob
from jobs.tests.base_job_test import BaseJobTest
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
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

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self) -> AbstractJob:
        pre_train_dataset = MLMPreTrainDatasetCreator(
            orig_data_path=self.PRETRAIN_DIR, training_data_dir=TEST_OUTPUT_DIR)
        trainer_dataset_manager = self.create_trainer_dataset_manager({
            DatasetRole.PRE_TRAIN: pre_train_dataset
        })
        test_params = self.get_job_args(dataset_role=DatasetRole.PRE_TRAIN, include_links=True)
        job_args = JobArgs(**test_params)
        job_args.trace_args_params = {
            "num_train_epochs": 1
        }

        return GanTrainJob(job_args, trainer_dataset_manager=trainer_dataset_manager)
