from typing import List, Dict

from test.jobs.health_check_jobs.health_check_utils import get_dataset_for_health_checks, QUERY_ID, CONCEPT_LAYER_ID, \
    mocks_for_health_checks, assert_health_check_success
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.health_check_jobs.health_check_job import HealthCheckJob
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHealthCheckJobJob(BaseJobTest):

    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager):
        """
        Tests that job is completed successfully.
        """
        mocks_for_health_checks(ai_manager)
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        result: HealthCheckResults = job_result.body
        assert_health_check_success(self, result)

    def _get_job(self, additional_chats: List[Dict] = None) -> AbstractJob:
        dataset = get_dataset_for_health_checks()
        return HealthCheckJob(JobArgs(dataset=dataset), query_id=QUERY_ID, concept_layer_id=CONCEPT_LAYER_ID)
