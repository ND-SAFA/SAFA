from unittest import mock
from unittest.mock import patch

from experiments.experiment import Experiment
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob


class TestExperiment(BaseExperimentTest):

    @patch.object(PredictJob, "_run")
    @patch.object(TrainJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock, predict_job_run_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        predict_job_run_mock.side_effect = self.job_fake_run
        experiment = self.get_experiment()
        experiment.run()
        self.assertEqual(train_job_run_mock.call_count, 8)
        self.assertEqual(predict_job_run_mock.call_count, 1)

    def get_experiment(self):
        return Experiment.initialize_from_definition(self.EXPERIMENT_DEFINITION)
