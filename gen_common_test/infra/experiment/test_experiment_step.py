from unittest import mock
from unittest.mock import patch

from gen_common.data.readers.definitions.structure_project_definition import StructureProjectDefinition
from gen_common.data.readers.structured_project_reader import StructuredProjectReader
from gen_common.infra.experiment.experiment_step import ExperimentStep
from gen_common.infra.experiment.object_creator import ObjectCreator
from gen_common.util.status import Status
from gen_common_test.infra.dummy_job import DummyJob
from gen_common_test.infra.experiment.base_experiment_test import BaseExperimentTest


class TestExperimentStep(BaseExperimentTest):
    EXPERIMENT_VARS = ["trainer_dataset_manager.train_dataset_creator.project_path",
                       "trainer_args.num_train_epochs"]

    def test_get_failed_jobs(self):
        jobs = self.get_test_jobs()
        jobs[0].result.status = Status.FAILURE
        failed_jobs = ExperimentStep._get_failed_jobs(jobs)
        self.assertEqual(1, len(failed_jobs))

    @patch.object(StructuredProjectReader, "get_definition_reader")
    def test_run_on_all_jobs(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        jobs = self.get_test_jobs()
        results = ExperimentStep._run_on_jobs(jobs, "get_output_filepath")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])  # Nothing differentiating the two paths other than id which is set by experiment

    @staticmethod
    def get_experiment_step(train=True) -> ExperimentStep:
        kwargs = {
            "override": True,
            **{
                "jobs": [{
                    **ObjectCreator.experiment_predict_job_definition,
                    "model_manager": {
                        "model_path": "?"
                    }
                }]
            }
        }
        return ObjectCreator.create(ExperimentStep, **kwargs)

    @staticmethod
    def get_job_by_id(step, job_id):
        found_job = None
        for job in step.jobs:
            if str(job.id) == job_id:
                found_job = job
                break
        return found_job

    @staticmethod
    def get_test_jobs():
        job1 = DummyJob()
        job2 = DummyJob()
        return [job1, job2]
