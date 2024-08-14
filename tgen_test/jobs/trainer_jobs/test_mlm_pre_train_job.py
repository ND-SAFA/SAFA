from common_resources.llm.args.hugging_face_args import HuggingFaceArgs

from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelTask
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.test_assertions import TestAssertions


class TestMLMPreTrainJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _test_run_success(self):
        job = self.get_job()
        job.run()
        self.assert_output_on_success(job, self._load_job_output(job))

    def _assert_success(self, job: HuggingFaceJob, output_dict: dict):
        TestAssertions.assert_training_output_matches_expected(self, output_dict)

    def _get_job(self):
        job_args = ObjectCreator.create(JobArgs)
        model_manager = ObjectCreator.create(ModelManager, **{
            "model_task": ModelTask.MASKED_LEARNING,
            "model_path": BaseJobTest.BASE_TEST_MODEL
        })
        trainer_dataset_manager = ObjectCreator.create(TrainerDatasetManager, **{
            "train_dataset_creator": ObjectCreator.pretrain_dataset_definition
        }, override=True)
        trainer_args = ObjectCreator.create(HuggingFaceArgs, evaluation_strategy="no", save_strategy="no")
        return HuggingFaceJob(model_manager=model_manager, trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args,
                              job_args=job_args, task=TrainerTask.PRE_TRAIN)
