import os
from unittest import mock
from unittest.mock import patch

from experiments.experiment import Experiment
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob
from test.test_object_creator import TestObjectCreator


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
        result_dirs = os.listdir(os.path.join(experiment.output_dir, str(experiment.id)))
        self.assertEquals(len(result_dirs), len(experiment.steps))

    def get_experiment(self):
        # return TestObjectCreator.create(Experiment)
        return Experiment.initialize_from_definition(self.EXPERIMENT_DEFINITION)
