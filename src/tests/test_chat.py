from test.jobs.health_check_jobs.health_check_utils import mocks_for_health_checks, get_dataset_for_health_checks, QUERY_ID, \
    CONCEPT_LAYER_ID, assert_health_check_success, get_dataset_for_context, QUERY, assert_correct_related_artifacts
from tests.base_test import BaseTest
from tests.common.request_proxy import RequestProxy
from tests.common.test_data import TestData, TestSubset
from tgen.data.exporters.api_exporter import ApiExporter
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, Message
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestChat(BaseTest):
    RESPONSE = "You should get a cat!"

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        :param ai_manager: The AI manages used to mock responses.
        :return: None
        """
        ai_manager.set_responses([self.RESPONSE])
        prompt_dataset = get_dataset_for_context()
        artifacts = prompt_dataset.artifact_df.to_artifacts()
        dataset = ApiDefinition(artifacts=artifacts)
        chat_history = [Message(content=QUERY[ArtifactKeys.CONTENT], role="user")]
        response = RequestProxy.chat(dataset, chat_history)
        self.assertEqual(response["response"], self.RESPONSE)
        assert_correct_related_artifacts(self, response["related_artifacts"])
