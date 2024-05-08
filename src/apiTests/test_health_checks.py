from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy

from test.jobs.health_check_jobs.health_check_utils import CONCEPT_LAYER_ID, QUERY_ID, assert_health_check_success, \
    get_dataset_for_health_checks, mocks_for_health_checks
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHealthChecks(BaseTest):

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        :param ai_manager: The AI manages used to mock responses.
        :return: None
        """
        prompt_dataset = get_dataset_for_health_checks()
        artifacts = prompt_dataset.artifact_df.to_artifacts()
        dataset = ApiDefinition(artifacts=artifacts)
        mocks_for_health_checks(ai_manager)
        response = RequestProxy.health(dataset, QUERY_ID, CONCEPT_LAYER_ID)
        assert_health_check_success(self, response)
