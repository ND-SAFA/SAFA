import os
from unittest import mock
from unittest.mock import patch

from config.override import overrides
from jobs.job_args import JobArgs
from jobs.train_job import TrainJob
from jobs.tests.base_job_test import BaseJobTest
from test.paths.paths import TEST_DATA_DIR
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.train.trace_trainer import TraceTrainer


class TestTrainJob(BaseJobTest):
    CSV_DATA_DIR = os.path.join(TEST_DATA_DIR, "csv")
    CSV_DATA_FILE = os.path.join(CSV_DATA_DIR, "test_csv_data.csv")

    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def test_split_train_dataset(self):
        job = self._get_job()
        self.assertTrue(job.trace_args.trainer_dataset_container.eval_dataset is not None)

    @staticmethod
    @overrides(BaseJobTest)
    def create_dataset_map(dataset_role: DatasetRole, include_links=True):
        train_dataset = BaseJobTest.create_dataset_map(DatasetRole.TRAIN)
        test_dataset = {DatasetRole.EVAL: (SupportedDatasetCreator.CSV, {"data_file_path": TestTrainJob.CSV_DATA_FILE})}
        return {**train_dataset, **test_dataset}

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self) -> TrainJob:
        test_params = self.get_test_params_for_trace(dataset_role=DatasetRole.TRAIN, include_links=True, split_train_dataset=True)
        job_args = JobArgs(**test_params)
        job = TrainJob(job_args)
        self.assertEquals(job.trace_args.num_train_epochs, 1)
        return job
