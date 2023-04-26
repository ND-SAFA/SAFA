import mock.mock

from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.util.open_ai_util import OpenAiUtil


class TestOpenAiUtil(BaseTest):

    @mock.patch("openai.Completion.create")
    def test_completion_request(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        res = OpenAiUtil.make_completion_request(model="ada", prompt=["prompt" for i in range(30)])
        self.assertEqual(len(res.choices), 30)
