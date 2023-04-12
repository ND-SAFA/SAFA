import ast
import os

from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.util.file_util import FileUtil


class TestPythonChunker(BaseTest):
    DATA_PATH = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
    MODEL = "code-cushman-001"

    def test_chunk(self):
        chunker = self.get_chunker()
        chunks = chunker.chunk(self.DATA_PATH)
        all_content = FileUtil.read_file(self.DATA_PATH).split("\n")
        chunked_content = "\n".join(chunks)
        for line in all_content:
            line = line.strip()
            if line.startswith("import") or line.startswith("from") or line.startswith("@") or not line:
                continue
            if line not in chunked_content:
                self.fail("Line %s in original file is missing from chunked content" % line)
        for chunk in chunks:
            if PythonChunker.estimate_num_tokens(chunk, self.MODEL) > chunker.token_limit:
                self.fail("Chunk exceeds token limit")

    def test_exceeds_token_limit(self):
        chunker = self.get_chunker()
        words = "word" * chunker.token_limit
        self.assertTrue(chunker.exceeds_token_limit(words))
        self.assertFalse(chunker.exceeds_token_limit("word"))

    def test_resize_node(self):
        chunker = self.get_chunker()
        class_def = ast.ClassDef()
        class_def.lineno = 1
        words = "word " * chunker.token_limit
        lines = words.split()
        class_def.end_lineno = len(lines)-1
        orig_content = chunker._get_node_content(class_def, lines)
        self.assertTrue(chunker.exceeds_token_limit(orig_content))
        resized_class_def = chunker._resize_node(class_def, lines)
        new_content = chunker._get_node_content(resized_class_def, lines)
        self.assertFalse(chunker.exceeds_token_limit(new_content))

    def test_get_node_content(self):
        class_def = ast.ClassDef()
        class_def.lineno = 1
        words = "word " * 2000
        lines = words.split()
        class_def.end_lineno = 4
        content = PythonChunker._get_node_content(class_def, lines)
        self.assertEqual(len(content.split("\n")), 4)

    def test_node2use(self):
        self.assertTrue(PythonChunker._node2use(ast.ClassDef()))
        self.assertFalse(PythonChunker._node2use(ast.Import()))

    def test_replace_white_space_with_tab(self):
        str_one_tab = PythonChunker._replace_white_space_with_tab("    test ")
        self.assertTrue(str_one_tab.startswith("\t"))
        self.assertEqual(str_one_tab.find("\t", 1), -1)
        str_two_tabs = PythonChunker._replace_white_space_with_tab("        test ")
        self.assertTrue(str_two_tabs.startswith("\t\t"))
        self.assertEqual(str_two_tabs.find("\t", 2), -1)
        str_no_tab = PythonChunker._replace_white_space_with_tab(" test ")
        self.assertEqual(str_no_tab.find("\t"), -1)

    def get_chunker(self):
        return PythonChunker(self.MODEL)
