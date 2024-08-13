from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.tools.variables.typed_definition_variable import TypedDefinitionVariable

from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.models.model_manager import ModelManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.test_assertions import TestAssertions


class TestPredictJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        job_args: JobArgs = ObjectCreator.create(JobArgs)
        model_manager: ModelManager = ObjectCreator.create(ModelManager)
        trainer_dataset_manager: TrainerDatasetManager = ObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            }
        }, override=True)
        trainer_args: HuggingFaceArgs = ObjectCreator.create(HuggingFaceArgs)
        return HuggingFaceJob(job_args=job_args, model_manager=model_manager, task=TrainerTask.PREDICT,
                              trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)

    def _assert_success(self, job: HuggingFaceJob, output_dict: dict):
        eval_dataset = job.trainer_dataset_manager[DatasetRole.EVAL]
        TestAssertions.verify_prediction_output(self, output_dict, eval_dataset)
