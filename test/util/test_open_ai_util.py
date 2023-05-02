import mock.mock

from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.util.llm.llm_responses import GenerationResponse
from tgen.util.llm.llm_task import LLMTask
from tgen.util.llm.open_ai_util import OpenAIUtil


class TestOpenAiUtil(BaseTest):
    """
    Tests the OpenAi Utility class.
    """

    @mock.patch("openai.Completion.create")
    def test_completion_request(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        res: GenerationResponse = OpenAIUtil.make_completion_request(task=LLMTask.GENERATION, model="ada",
                                                                     prompt=["prompt" for i in range(30)])
        self.assertEqual(len(res.batch_responses), 30)
