from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_args import JobArgs
from jobs.tests.base_job_test import BaseJobTest
from jobs.vsm_job import VSMJob
from testres.test_assertions import TestAssertions
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestVSMJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def _get_job(self):
        job_args: JobArgs = ObjectCreator.create(JobArgs)
        trainer_dataset_manager: TrainerDatasetManager = ObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            }
        }, override=False)
        return VSMJob(job_args, trainer_dataset_manager=trainer_dataset_manager,
                      metrics=ObjectCreator.trainer_args_definition["metrics"])

    def _assert_success(self, job: VSMJob, output_dict: dict):
        eval_dataset = job.trainer_dataset_manager[DatasetRole.EVAL]
        TestAssertions.verify_prediction_output(self, output_dict, eval_dataset, base_score=0.0)
