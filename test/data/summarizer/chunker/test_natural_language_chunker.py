from tgen.data.summarizer.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.testres.base_tests.base_test import BaseTest


class TestNaturalLanguageChunker(BaseTest):

    def test_chunk(self):
        n_times_limit = 3
        chunker = NaturalLanguageChunker("ada")
        long_text = "Hello " * (n_times_limit*round(chunker.token_limit / 4))
        chunks = chunker.chunk(long_text)
        self.assertEqual(len(chunks), n_times_limit)
        self.assertEqual(" ".join(chunks) + " ", long_text)
