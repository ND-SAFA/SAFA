from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.testres.base_tests.base_test import BaseTest


class TestSupportedChunker(BaseTest):

    def test_get_chunker(self):
        self.assertEqual(SupportedChunker.determine_from_ext("file.py"), SupportedChunker.PY)
        self.assertEqual(SupportedChunker.determine_from_ext("file.java"), SupportedChunker.JAVA)
        self.assertEqual(SupportedChunker.determine_from_ext("file.txt"), SupportedChunker.NL)
        self.assertEqual(SupportedChunker.determine_from_ext(), SupportedChunker.NL)