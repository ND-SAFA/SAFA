from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_args import JobArgs
from jobs.mlm_pre_train_job import MLMPreTrainJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from models.model_properties import ModelTask
from test.test_assertions import TestAssertions
from train.trainer_args import TrainerArgs
from util.object_creator import TestObjectCreator


class TestMLMPreTrainJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _test_run_success(self):
        job = self.get_job()
        job.run()
        self.assert_output_on_success(self._load_job_output(job))

    def _assert_success(self, output_dict: dict):
        TestAssertions.assert_training_output_matches_expected(self, output_dict)

    def _get_job(self):
        job_args = TestObjectCreator.create(JobArgs)
        model_manager = TestObjectCreator.create(ModelManager, **{
            "model_task": ModelTask.MASKED_LEARNING,
            "model_path": "bert-base-uncased"
        })
        trainer_dataset_manager = TestObjectCreator.create(TrainerDatasetManager, **{
            "train_dataset_creator": TestObjectCreator.pretrain_dataset_definition
        }, override=True)
        trainer_args = TestObjectCreator.create(TrainerArgs)
        return MLMPreTrainJob(job_args=job_args, model_manager=model_manager,
                              trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)
