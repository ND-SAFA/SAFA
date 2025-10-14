from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from gen_common.data.readers.definitions.api_definition import ApiDefinition
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_test.health.health_check_constants import QUERY_ID, CONCEPT_LAYER_ID
from gen_test.health.health_check_utils import get_dataset_for_health_checks, assert_health_check_success


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
        # TODO: mocks_for_health_checks(ai_manager)
        response = RequestProxy.health(dataset, QUERY_ID, CONCEPT_LAYER_ID)
        assert_health_check_success(self, response)
