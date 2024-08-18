from typing import Dict, List

from gen_common.jobs.abstract_job import AbstractJob, JobResult
from gen_common.jobs.job_args import JobArgs
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_job_test import BaseJobTest

from gen.health.jobs.health_check_job import HealthCheckJob
from gen.health.jobs.health_check_results import HealthCheckResults
from gen_test.health.health_check_constants import CONCEPT_LAYER_ID, QUERY_ID
from gen_test.health.health_check_utils import assert_health_check_success, \
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
