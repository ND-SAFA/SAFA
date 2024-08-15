from tgen_test.data.chunker.constants import CHUNK_TEST_SENTENCE
from tgen_test.data.chunker.util import verify_test_chunks
from common_resources.data.objects.artifact import Artifact
from tgen.data.chunkers.sentence_chunker import SentenceChunker
from tgen.testres.base_tests.base_test import BaseTest


class TestSentenceChunker(BaseTest):

    def test_chunk(self):
        """
        Verifies that sentence chunker splits sentence by punctuation and all chunks start with capital.
        """
        artifact = Artifact(id=1, content=CHUNK_TEST_SENTENCE, layer_id="layer")
        chunks = SentenceChunker().chunk([artifact])[0]
        verify_test_chunks(self, chunks)
