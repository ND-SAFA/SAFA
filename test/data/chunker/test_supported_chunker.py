from tgen.data.chunkers.token_limit_chunkers.supported_chunker import SupportedChunker
from tgen.testres.base_tests.base_test import BaseTest


class TestSupportedChunker(BaseTest):

    def test_get_chunker(self):
        self.assertEqual(SupportedChunker.determine_from_path("file.py"), SupportedChunker.PY)
        self.assertEqual(SupportedChunker.determine_from_path("file.java"), SupportedChunker.JAVA)
        self.assertEqual(SupportedChunker.determine_from_path("file.cpp"), SupportedChunker.CODE)
        self.assertEqual(SupportedChunker.determine_from_path("file.txt"), SupportedChunker.NL)
        self.assertEqual(SupportedChunker.determine_from_path(), SupportedChunker.NL)

        self.assertEqual(SupportedChunker.get_chunker_from_ext("file.java"), SupportedChunker.JAVA)
