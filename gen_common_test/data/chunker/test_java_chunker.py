import os

from gen_common.data.chunkers.token_limit_chunkers.java_chunker import JavaChunker
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.data.chunker.base_code_chunker_test import BaseCodeChunkerTest
from gen_common_test.paths.base_paths import TEST_DATA_DIR


class TestJavaChunker(BaseTest):
    BASE_DATA_PATH = os.path.join(TEST_DATA_DIR, "chunker")
    DATA_PATH = os.path.join(BASE_DATA_PATH, "test_java.java")
    MODEL = "code-cushman-001"

    def test_chunk(self):
        BaseCodeChunkerTest.verify_chunk(self, self.get_chunker(), is_line_2_ignore=lambda line: line.startswith("import")
                                                                                                 or line.startswith("package"),
                                         line_overrides=lambda line: line == '}')

    def test_common_methods(self):
        BaseCodeChunkerTest.verify_common_methods(self, self.get_chunker())

    def get_chunker(self):
        chunker = JavaChunker(self.MODEL, 1000)
        return chunker
