import os
from unittest import mock
from unittest.mock import patch

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from experiments.experiment_step import ExperimentStep
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.components.job_result import JobResult
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob
from test.paths.paths import TEST_OUTPUT_DIR
from test.test_object_creator import TestObjectCreator
from util.status import Status


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
        train_experiment_step = self.get_experiment_step(train_job=True)
        predict_experiment_step = self.get_experiment_step(train_job=False)
        best_job_from_prior = train_experiment_step.jobs.pop()
        best_job = predict_experiment_step.run([best_job_from_prior]).pop()
        self.assertEquals(best_job.model_manager.model_path, best_job_from_prior.model_manager.model_path)
        self.assertEqual(predict_job_run_mock.call_count, 1)

    def get_experiment_step(self, train_job=True):
        if train_job:
            step = TestObjectCreator.create(ExperimentStep)
        else:
            step = TestObjectCreator.create(ExperimentStep, override=True,
                                            **TestObjectCreator.experiment_predict_step_definition)
        return step

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
