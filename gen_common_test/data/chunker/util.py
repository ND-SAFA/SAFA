from typing import List
from unittest import TestCase

from gen_common.util.str_util import StrUtil
from gen_common_test.data.chunker.constants import CHUNK_TEST_SENTENCE


def verify_test_chunks(tc: TestCase, result_chunks: List[str], expected_chunks: List[str] = None) -> None:
    """
    Verifies that resulting chunks match expected chunks.
    :param tc: Test case to make assertions with.
    :param result_chunks: Chunks to verify.
    :param expected_chunks: Expected chunks, defaults to chunks from CHUNK_TEST_SENTENCE.
    :return: None
    """
    if expected_chunks is None:
        expected_chunks = get_test_chunks()
    tc.assertEqual(len(result_chunks), len(expected_chunks))
    for sentence in result_chunks:
        tc.assertTrue(sentence[0].isupper())  # all sentences start with a capital


def get_test_chunks() -> List[str]:
    """
    :return: Chunks in test sentence.
    """
    return StrUtil.split_by_punctuation(CHUNK_TEST_SENTENCE)
