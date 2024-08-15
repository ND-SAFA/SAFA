from common_resources.tools.constants.symbol_constants import NEW_LINE

from common_resources.data.objects.artifact import Artifact
from common_resources.tools.util.prompt_util import PromptUtil
from tgen.data.chunkers.llm_chunker import LLMChunker
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager
from tgen_test.data.chunker.constants import CHUNK_TEST_SENTENCE
from tgen_test.data.chunker.util import get_test_chunks, verify_test_chunks


class TestLLMChunker(BaseTest):

    @mock_anthropic
    def test_chunk(self, mock_ai: TestAIManager):
        """
        Chunks sentence and verifies that each chunk was accurately computed.
        """
        expected_chunks = get_test_chunks()
        mock_ai.set_responses([NEW_LINE.join([PromptUtil.create_xml("chunk", chunk) for chunk in expected_chunks])])
        artifact = Artifact(id=1, content=CHUNK_TEST_SENTENCE, layer_id="layer")
        chunks = LLMChunker().chunk([artifact])[0]
        verify_test_chunks(self, chunks, expected_chunks=expected_chunks)
