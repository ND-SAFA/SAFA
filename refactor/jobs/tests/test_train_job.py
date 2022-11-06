from unittest import mock
from unittest.mock import patch

from jobs.train_job import TrainJob
from test.base_job_test import BaseJobTest
from tracer.dataset.dataset_role import DatasetRole
from tracer.train.trace_trainer import TraceTrainer


class TestTrainJob(BaseJobTest):
    TEST_PARAMS = BaseJobTest.get_test_params_with_dataset(dataset_role=DatasetRole.TRAIN, include_links=True)

    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _assert_success(self, output_dict: dict):
        self.assert_training_output_matches_expected(output_dict)

    def _get_job(self):
        return TrainJob(**self.TEST_PARAMS, split_train_dataset=True)
