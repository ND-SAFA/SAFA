from typing import List

from api.endpoints.gen.serializers.message_serializer import MessageDTO
from api.server.app_endpoints import AppEndpoints
from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.readers.definitions.api_definition import ApiDefinition

from gen_common.util.prompt_util import PromptUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_test.health.health_check_constants import QUERY
from gen_test.health.health_check_utils import get_dataset_for_context


class TestChatTitle(BaseTest):

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        Tests that chat is able to be anam.ed
        """
        expected_title = "chat title"
        ai_manager.set_responses([PromptUtil.create_xml("title", expected_title)])
        prompt_dataset = get_dataset_for_context()
        artifacts = prompt_dataset.artifact_df.to_artifacts()
        dataset = ApiDefinition(artifacts=artifacts)
        chat_history: List[MessageDTO] = [
            {"artifact_ids": set(), "role": "user", "content": QUERY[ArtifactKeys.CONTENT]},
            {"artifact_ids": set(), "role": "assistant", "content": "blah blah"}
        ]
        response = RequestProxy.chat(dataset, chat_history, AppEndpoints.CHAT_TITLE)
        self.assertEqual(response["title"], "chat title")
