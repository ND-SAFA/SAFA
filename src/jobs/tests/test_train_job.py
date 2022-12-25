import os
from unittest import mock
from unittest.mock import patch

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.dataset_role import DatasetRole
from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from experiments.variables.typed_definition_variable import TypedDefinitionVariable
from jobs.components.job_args import JobArgs
from jobs.tests.base_job_test import BaseJobTest
from jobs.train_job import TrainJob
from models.model_manager import ModelManager
from test.paths.paths import TEST_DATA_DIR
from test.test_assertions import TestAssertions
from test.test_object_creator import TestObjectCreator
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs


class TestTrainJob(BaseJobTest):
    CSV_DATA_DIR = os.path.join(TEST_DATA_DIR, "csv")
    CSV_DATA_FILE = os.path.join(CSV_DATA_DIR, "test_csv_data.csv")
    EXPECTED_SPLIT_ROLE: DatasetRole = DatasetRole.EVAL

    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def test_split_train_dataset(self):
        job = self._get_job()
        self.assertTrue(job.trainer_dataset_manager[self.EXPECTED_SPLIT_ROLE] is not None)

    def _assert_success(self, output_dict: dict):
        TestAssertions.assert_training_output_matches_expected(self, output_dict)

    def _get_job(self) -> TrainJob:
        job_args: JobArgs = TestObjectCreator.create(JobArgs)
        trainer_args: TrainerArgs = TestObjectCreator.create(TrainerArgs)
        dataset_param = "_".join([self.EXPECTED_SPLIT_ROLE.value, "dataset", "creator"])
        trainer_dataset_manager: TrainerDatasetManager = TestObjectCreator.create(TrainerDatasetManager, **{
            dataset_param: {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": VALIDATION_PERCENTAGE_DEFAULT
            }
        })
        model_manager: ModelManager = TestObjectCreator.create(ModelManager)
        job = TrainJob(job_args,
                       trainer_dataset_manager=trainer_dataset_manager,
                       trainer_args=trainer_args,
                       model_manager=model_manager)
        self.assertEquals(job.trainer_args.num_train_epochs, 1)
        return job
