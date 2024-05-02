from test.jobs.health_check_jobs.health_check_utils import mocks_for_health_checks, get_dataset_for_health_checks, QUERY_ID, \
    CONCEPT_LAYER_ID, assert_health_check_success
from tests.base_test import BaseTest
from tests.common.request_proxy import RequestProxy
from tests.common.test_data import TestData, TestSubset
from tgen.data.exporters.api_exporter import ApiExporter
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHealthChecks(BaseTest):

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        Traces between the source and target artifacts of test dataset.
        :param ai_manager: The AI manages used to mock responses.
        :return: None
        """
        prompt_dataset = get_dataset_for_health_checks()
        artifacts = prompt_dataset.artifact_df.to_artifacts()
        dataset = ApiDefinition(artifacts=artifacts)
        mocks_for_health_checks(ai_manager)
        response = RequestProxy.health(dataset, QUERY_ID, CONCEPT_LAYER_ID)
        assert_health_check_success(self, response)
