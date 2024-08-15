from typing import Dict, List

from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager

from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.health_check_jobs.health_check_job import HealthCheckJob
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen_test.jobs.health_check_jobs.health_check_constants import CONCEPT_LAYER_ID, QUERY_ID
from tgen_test.jobs.health_check_jobs.health_check_utils import assert_health_check_success, \
    get_dataset_for_health_checks, mocks_for_health_checks


class TestHealthCheckJob(BaseJobTest):

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
        return HealthCheckJob(JobArgs(dataset=dataset), query_ids=[QUERY_ID], concept_layer_id=CONCEPT_LAYER_ID)
