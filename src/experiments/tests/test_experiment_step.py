from unittest import mock
from unittest.mock import patch

from experiments.experiment_step import ExperimentStep
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.components.job_result import JobResult
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob
from test.test_object_creator import TestObjectCreator


class TestExperimentStep(BaseExperimentTest):

    @patch.object(TrainJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        experiment_step = self.get_experiment_step()
        best_job = experiment_step.run().pop()
        self.assertEquals(max(self.accuracies), best_job.result[JobResult.METRICS]["accuracy"])
        self.assertEqual(train_job_run_mock.call_count, 8)

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
            step_definition = self.EXPERIMENT_DEFINITION["steps"][0]
        else:
            step = TestObjectCreator.create(ExperimentStep, override=True, **TestObjectCreator.experiment_predict_step_definition)
            step_definition = self.EXPERIMENT_DEFINITION["steps"][1]
        step = ExperimentStep.initialize_from_definition(step_definition)
        return step
