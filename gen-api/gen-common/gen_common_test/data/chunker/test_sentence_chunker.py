from gen_common.data.chunkers.sentence_chunker import SentenceChunker
from gen_common.data.objects.artifact import Artifact
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.data.chunker.constants import CHUNK_TEST_SENTENCE
from gen_common_test.data.chunker.util import verify_test_chunks


class TestSentenceChunker(BaseTest):

    def test_chunk(self):
        """
        Verifies that sentence chunker splits sentence by punctuation and all chunks start with capital.
        """
        artifact = Artifact(id=1, content=CHUNK_TEST_SENTENCE, layer_id="layer")
        chunks = SentenceChunker().chunk([artifact])[0]
        verify_test_chunks(self, chunks)
