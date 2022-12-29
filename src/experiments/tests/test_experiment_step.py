import math
import os
from unittest import mock
from unittest.mock import patch

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from experiments.experiment_step import ExperimentStep
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.delete_model_job import DeleteModelJob
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator
from util.status import Status
from variables.undetermined_variable import UndeterminedVariable


class TestExperimentStep(BaseExperimentTest):
    EXPERIMENT_VARS = ["trainer_dataset_manager.train_dataset_creator.project_path",
                       "trainer_args.num_train_epochs"]

    @patch.object(TrainJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        experiment_step = self.get_experiment_step()
        experiment_step.run()
        experiment_step.save_results(TEST_OUTPUT_DIR)
        output = self._load_step_output(experiment_step)
        result_dirs = os.listdir(os.path.join(TEST_OUTPUT_DIR))
        for job_id in output["jobs"]:
            self.assertIn(job_id, result_dirs)
        self.assert_experimental_vars(output, experiment_step)
        self.assertEquals(output["status"], Status.SUCCESS.value)
        best_job = self.get_job_by_id(experiment_step, output["best_job"])
        self.assertTrue(best_job is not None)
        self.assertEquals(max(self.accuracies), best_job.result[JobResult.METRICS]["accuracy"])
        self.assertEqual(train_job_run_mock.call_count, 4)

    @patch.object(PredictJob, "_run")
    def test_run_with_best_prior(self, predict_job_run_mock: mock.MagicMock):
        predict_job_run_mock.side_effect = self.job_fake_run
        train_experiment_step = self.get_experiment_step()
        predict_experiment_step = self.get_experiment_step(train=False)
        best_job_from_prior = train_experiment_step.jobs.pop()
        best_job = predict_experiment_step.run([best_job_from_prior]).pop()
        expected_model_path = best_job_from_prior.model_manager.model_path
        self.assertEquals(best_job.model_manager.model_path, expected_model_path)
        self.assertEqual(predict_job_run_mock.call_count, 1)

    def test_divide_jobs_into_runs(self):
        train_step = self.get_experiment_step()
        runs = train_step._divide_jobs_into_runs()
        self.assertEquals(len(runs), math.ceil(len(train_step.jobs) / train_step.MAX_JOBS))
        for run_ in runs:
            self.assertLessEqual(len(run_), train_step.MAX_JOBS)

    def test_update_jobs_undetermined_vars(self):
        train_step = self.get_experiment_step()
        predict_step = self.get_experiment_step(train=False)
        predict_step.jobs[0].trainer_args.num_train_epochs = UndeterminedVariable()
        final_jobs = predict_step._update_jobs_undetermined_vars(predict_step.jobs, train_step.jobs)
        self.assertEquals(len(final_jobs), len(train_step.jobs))
        for job in final_jobs:
            self.assertTrue(not isinstance(job.trainer_args.num_train_epochs, UndeterminedVariable))
            self.assertTrue(not isinstance(job.model_manager.model_path, UndeterminedVariable))

    def test_run_on_all_jobs(self):
        jobs = self.get_test_jobs()
        results = ExperimentStep._run_on_jobs(jobs, "get_output_filepath")
        self.assertEquals(len(results), 2)
        self.assertNotEquals(results[0], results[1])

    def test_get_best_job(self):
        job1, job2 = self.get_test_jobs()
        job1.result[JobResult.METRICS] = {"accuracy": 0.5}

        job2.result[JobResult.METRICS] = {"accuracy": 0.8}
        best_job = ExperimentStep._get_best_job([job1, job2], comparison_metric="accuracy")
        self.assertEquals(best_job.id, job2.id)

    def get_experiment_step(self, train=True):
        kwargs = {}
        if not train:
            kwargs = {"override": True, **{
                "jobs": [{
                    **ObjectCreator.experiment_predict_job_definition,
                    "model_manager": {
                        "model_path": "?"
                    }
                }]
            }}
        return ObjectCreator.create(ExperimentStep, **kwargs)

    @staticmethod
    def get_test_jobs():
        job1 = DeleteModelJob(job_args=JobArgs(output_dir=TEST_OUTPUT_DIR))
        job2 = DeleteModelJob(job_args=JobArgs(output_dir=TEST_OUTPUT_DIR))
        return [job1, job2]

    @staticmethod
    def get_job_by_id(step, job_id):
        found_job = None
        for job in step.jobs:
            if str(job.id) == job_id:
                found_job = job
                break
        return found_job

    def assert_experimental_vars(self, output, experiment_step):
        for job_id, job_experiment_vars in output["job_to_experimental_var"].items():
            for experiment_var_path in self.EXPERIMENT_VARS:
                path_attrs = experiment_var_path.split(".")
                attr = self.get_job_by_id(experiment_step, job_id)
                for i, attr_name in enumerate(path_attrs):
                    if not hasattr(attr, attr_name):
                        if isinstance(attr, TrainerDatasetManager):
                            attr = attr.get_creator(DatasetRole.TRAIN)
                        continue
                    attr = getattr(attr, attr_name)
                    self.assertIn(attr_name, job_experiment_vars.keys())
                    if i == len(path_attrs) - 1:
                        self.assertEquals(str(attr), job_experiment_vars[attr_name])
