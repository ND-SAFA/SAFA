import ast

from gen_common.data.chunkers.token_limit_chunkers.chunked_node import ChunkedNode
from gen_common.data.chunkers.token_limit_chunkers.python_chunker import PythonChunker
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_CHUNK_TESTPYTHON_PATH
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.data.chunker.base_code_chunker_test import BaseCodeChunkerTest


class TestPythonChunker(BaseTest):
    DATA_PATH = GEN_COMMON_TEST_PROJECT_CHUNK_TESTPYTHON_PATH
    MODEL = "code-cushman-001"

    @staticmethod
    def lines_to_ignore(line):
        return line.startswith("import") or line.startswith("from")

    def test_chunk(self):
        BaseCodeChunkerTest.verify_chunk(self, self.get_chunker(), self.lines_to_ignore, lambda line: line.startswith("@"))

    def test_common_methods(self):
        BaseCodeChunkerTest.verify_common_methods(self, self.get_chunker())

    def test_node2use(self):
        self.assertTrue(PythonChunker._is_node_2_use(ChunkedNode.from_python_ast(ast.ClassDef())))
        self.assertFalse(PythonChunker._is_node_2_use(ChunkedNode.from_python_ast(ast.Import())))

    def test_preprocess_line(self):
        str_one_tab = PythonChunker._preprocess_line("    test ")
        self.assertTrue(str_one_tab.startswith("\t"))
        self.assertEqual(str_one_tab.find("\t", 1), -1)
        str_two_tabs = PythonChunker._preprocess_line("        test ")
        self.assertTrue(str_two_tabs.startswith("\t\t"))
        self.assertEqual(str_two_tabs.find("\t", 2), -1)
        str_no_tab = PythonChunker._preprocess_line(" test ")
        self.assertEqual(str_no_tab.find("\t"), -1)

    def get_chunker(self):
        return PythonChunker(self.MODEL, 1000)
