from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.objects.artifact import Artifact
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.str_util import StrUtil
from tgen.data.chunkers.llm_chunker import LLMChunker
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestLLMChunker(BaseTest):

    @mock_anthropic
    def test_chunk(self, mock_ai: TestAIManager):
        content = "Here is 1.0 sentence. Here is another sentence; This sentence ends with an exclamation! " \
                  "This is a question? And one more. "
        chunked_content = StrUtil.split_by_punctuation(content)
        mock_ai.set_responses([NEW_LINE.join([PromptUtil.create_xml("chunk", chunk) for chunk in chunked_content])])
        artifact = Artifact(id=1, content=content, layer_id="layer")
        chunks = LLMChunker().chunk([artifact])[0]
        self.assertEqual(len(chunks), len(chunked_content))
        for sentence in chunks:
            self.assertTrue(sentence[0].isupper())  # all sentences start with a capital
