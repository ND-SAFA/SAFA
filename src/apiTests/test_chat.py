from typing import List

from api.endpoints.gen.serializers.message_serializer import MessageDTO
from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from test.jobs.health_check_jobs.health_check_utils import QUERY, assert_correct_related_artifacts, get_dataset_for_context
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.readers.definitions.api_definition import ApiDefinition
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
        chat_history: List[MessageDTO] = [
            {"artifact_ids": [], "role": "user", "content": QUERY[ArtifactKeys.CONTENT]}
        ]
        response = RequestProxy.chat(dataset, chat_history)
        self.assertEqual(response["message"], self.RESPONSE)
        assert_correct_related_artifacts(self, response["artifact_ids"])
