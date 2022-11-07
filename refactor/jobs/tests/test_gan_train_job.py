from unittest import mock
from unittest.mock import patch

from jobs.abstract_job import AbstractJob
from jobs.gan_train_job import GanTrainJob
from jobs.tests.test_train_job import TestTrainJob
from test.base_job_test import BaseJobTest
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.train.trace_trainer import TraceTrainer


class TestGanTrainJob(BaseJobTest):
    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    @staticmethod
    def create_dataset_map(dataset_role: DatasetRole, include_links=True):
        train_dataset = BaseJobTest.create_dataset_map(DatasetRole.TRAIN)
        test_dataset = {DatasetRole.EVAL: (SupportedDatasetCreator.CSV, {"data_file_path": TestTrainJob.CSV_DATA_FILE})}
        return {**train_dataset, **test_dataset}

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self) -> AbstractJob:
        test_params = self.get_test_params_for_trace(dataset_role=DatasetRole.PRE_TRAIN, include_links=True)
        job = GanTrainJob(**test_params)
        return job
