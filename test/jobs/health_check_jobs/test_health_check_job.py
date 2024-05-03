from typing import List, Dict

from test.concepts.test_entity_extraction import TestEntityExtraction
from test.concepts.test_entity_matching import TestEntityMatching
from test.jobs.health_check_jobs.health_check_utils import ARTIFACT_IDS, EXPECTED_CONTEXT_IDS, assert_correct_related_traces, \
    get_dataset_for_context, get_dataset_for_health_checks, QUERY_ID, CONCEPT_LAYER_ID, EXPECTED_CONTRADICTION, \
    EXPECTED_RELATED_ARTIFACTS, QUERY_CONCEPTS, EXISTING_CONCEPTS, mocks_for_health_checks, assert_health_check_success
from tgen.common.objects.artifact import Artifact
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.health_check_jobs.health_check_job import HealthCheckJob
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
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
        assert_health_check_success(self, DataclassUtil.convert_to_dict(result))

    def _get_job(self, additional_chats: List[Dict] = None) -> AbstractJob:
        dataset = get_dataset_for_health_checks()
        return HealthCheckJob(JobArgs(dataset=dataset), query_id=QUERY_ID, concept_layer_id=CONCEPT_LAYER_ID)
