
from jobs.predict_job import PredictJob
from test.base_job_test import BaseJobTest
from tracer.dataset.dataset_role import DatasetRole


class TestPredictJob(BaseJobTest):
    TEST_PARAMS = BaseJobTest.get_test_params_with_dataset(dataset_role=DatasetRole.EVAL, include_links=False)

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        return PredictJob(**self.TEST_PARAMS)

    def _assert_success(self, output_dict: dict):
        self.assert_prediction_output_matches_expected(output_dict)
