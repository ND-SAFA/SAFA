from tgen.common.objects.artifact import Artifact
from tgen.data.chunkers.sentence_chunker import SentenceChunker
from tgen.testres.base_tests.base_test import BaseTest


class TestSentenceChunker(BaseTest):

    def test_chunk(self):
        content = "Here is 1.0 sentence. Here is another sentence; This sentence ends with an exclamation! " \
                  "This is a question? And one more. "
        artifact = Artifact(id=1, content=content, layer_id="layer")
        chunks = SentenceChunker().chunk([artifact])[0]
        self.assertEqual(len(chunks), 5)
        for sentence in chunks:
            self.assertTrue(sentence[0].isupper())  # all sentences start with a capital
