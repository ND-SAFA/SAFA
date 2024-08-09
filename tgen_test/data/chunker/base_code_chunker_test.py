from collections import Counter
from typing import Callable

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.file_util import FileUtil
from tgen.data.chunkers.token_limit_chunkers.chunked_node import ChunkedNode
from tgen.models.tokens.token_calculator import TokenCalculator


class BaseCodeChunkerTest:

    @staticmethod
    def verify_exceeds_token_limit(test, chunker):
        """
        Verifies that exceeds token limit is correct
        :param test: The test calling the method
        :param chunker: Chunker to test
        """
        words = "word" * (chunker.max_prompt_tokens * 2)
        test.assertTrue(chunker.exceeds_token_limit(words))
        test.assertFalse(chunker.exceeds_token_limit("word"))

    @staticmethod
    def verify_resize_node(test, chunker):
        """
        Verifies that the node is properly resized
        :param test: The test calling the method
        :param chunker: Chunker to test
        """
        words = "word " * chunker.max_prompt_tokens
        lines = words.split()
        class_def = ChunkedNode(lineno=1, end_lineno=len(lines) - 1, type="Class")
        orig_content = chunker._get_node_content(class_def, lines)
        test.assertTrue(chunker.exceeds_token_limit(orig_content))
        resized_class_def = chunker._resize_node(class_def, lines)
        new_content = chunker._get_node_content(resized_class_def, lines)
        test.assertFalse(chunker.exceeds_token_limit(new_content))

    @staticmethod
    def verify_get_node_content(test, chunker):
        """
        Verifies that the node content is correctly recovered
        :param test: The test calling the method
        :param chunker: Chunker to test
        """
        class_def = ChunkedNode(lineno=1, end_lineno=4, type="Class")
        words = "word " * 2000
        lines = words.split()
        content = chunker._get_node_content(class_def, lines)
        test.assertEqual(len(content.split(NEW_LINE)), 4)

    @staticmethod
    def verify_common_methods(test, chunker):
        """
        Verifies all common methods (except .chunk due to the additional params)
        :param test: The test calling the method
        :param chunker: Chunker to test
        """
        BaseCodeChunkerTest.verify_get_node_content(test, chunker)
        BaseCodeChunkerTest.verify_resize_node(test, chunker)
        BaseCodeChunkerTest.verify_exceeds_token_limit(test, chunker)

    @staticmethod
    def verify_chunk(test, chunker, is_line_2_ignore: Callable = None, line_overrides: Callable = None):
        """
        Verifies that the chunker performs chunking correctly
        :param test: The test calling the method
        :param chunker: The chunker to test
        :param is_line_2_ignore: Returns True if the line should be ignored by the chunker, else False
        :param line_overrides: Returns True if the line should not cause a test failure
        """
        content = FileUtil.read_file(test.DATA_PATH)
        chunks = chunker.chunk(content=content, id_=test.DATA_PATH)
        all_content = [line.strip() for line in content.split(NEW_LINE) if (is_line_2_ignore is None
                                                                            or not is_line_2_ignore(line.strip())) and line]
        all_content_line_counts = Counter(all_content)
        chunked_content = []
        for chunk in chunks:
            chunked_content.extend([line.strip() for line in chunk.split(NEW_LINE) if len(line.strip()) > 0])
        chunked_content_line_counts = Counter(chunked_content)

        differences = {}
        for line, count in all_content_line_counts.items():
            if line_overrides is not None and line_overrides(line):
                continue
            if line not in chunked_content_line_counts:
                differences[line] = count
            if chunked_content_line_counts[line] != count:
                differences[line] = count - chunked_content_line_counts[line]
        if len(differences) > 0:
            test.fail(f"The following differences were found between the original content and the chunked content\n {differences}")
        extra_tokens = []
        for i, chunk in enumerate(chunks):
            extra_token_count = TokenCalculator.estimate_num_tokens(chunk, test.MODEL) - chunker.max_prompt_tokens
            if extra_token_count >= 100:
                extra_tokens.append(extra_token_count)
        if len(extra_tokens) > 0:
            test.fail(f"{len(extra_tokens)} chunks exceeds token limit by following amounts: {extra_tokens}")
