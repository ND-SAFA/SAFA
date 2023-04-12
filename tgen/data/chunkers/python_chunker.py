import ast
import math
import os
import re
from typing import List, Union

import tiktoken

from tgen.data.chunkers.open_ai_token_limits import ModelTokenLimits
from tgen.util.file_util import FileUtil

NODE = Union[ast.AST, ast.stmt]


class PythonChunker:
    """
    Handles chunking for python files
    """

    IGNORED_NODES = [ast.Import, ast.ImportFrom]
    N_SPACE_TO_TAB = 4

    def __init__(self, model_name: str):
        """
        Initializes chunker with for a given model.
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        self.model_name = model_name
        self.token_limit = ModelTokenLimits.get_token_limit_for_model(self.model_name)

    def chunk(self, path_to_code: str) -> List[str]:
        """
        Chunks the given file into pieces that are beneath the model's token limit
        :param path_to_code: The path to the python file to chunk
        :return: The nodes chunked into sizes beneath the token limit
        """
        file_content = FileUtil.read_file(path_to_code)
        lines = [self._replace_white_space_with_tab(line) for line in file_content.split(os.linesep)]
        nodes = ast.parse(file_content)
        chunks = self.__chunk_helper(nodes, lines)
        return [self._get_node_content(chunk, lines) for chunk in chunks]

    def __chunk_helper(self, p_node: NODE, lines: List[str]) -> List[NODE]:
        """
        Performs the recursive chunking function to obtain chunks that are under the token limit
        :param p_node: The parent node
        :param lines: The lines from the code file
        :return: The nodes chunked into sizes under the token limit
        """
        c_nodes = p_node.body
        potential_chunks = [node for node in c_nodes if self._node2use(node)]
        chunks = []
        for chunk in potential_chunks:
            content = self._get_node_content(chunk, lines)
            if self.exceeds_token_limit(content):
                if len(chunk.body) < 1:
                    chunks.append(self._resize_node(chunk, lines))
                else:
                    new_chunks = self.__chunk_helper(chunk, lines)
                    chunk.end_lineno = new_chunks[0].lineno-2  # ensure no content from parent is lost
                    chunks.extend([chunk] + new_chunks)
            else:
                chunks.append(chunk)
        return chunks

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Returns true if the given content exceeds the token limit for the model.
        :param content: The content to check
        :return: True if the content exceeds the token limit for the model else False
        """
        return self.estimate_num_tokens(content, self.model_name) > self.token_limit

    @staticmethod
    def estimate_num_tokens(content: str, model_name: str) -> int:
        """
        Approximates the number of tokens that some content will be tokenized into by a given model.
        :param content: The content to be tokenized
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(content))
        return num_tokens

    def _resize_node(self, node: NODE, lines: List[str]) -> NODE:
        """
        Resizes the node to fit within the required number of tokens
        :return: The resized node
        """
        content = self._get_node_content(node, lines)
        while self.exceeds_token_limit(content):
            content = self._get_node_content(node, lines)
            node.end_lineno -= 1
            if node.end_lineno == node.lineno:
                break
        return node

    @staticmethod
    def _get_node_content(node: NODE, lines: List[str]) -> str:
        """
        Gets the content of the node
        :param node: The ast parsed node
        :param lines: The lines of the code file
        :return: The content of the node
        """
        start_lineno = node.lineno - 1
        end_lineno = node.end_lineno
        return os.linesep.join(lines[start_lineno:end_lineno])

    @staticmethod
    def _node2use(node: NODE) -> bool:
        """
        Determines if the node is a part of the hierarchy used for chunking
        :param node: The node
        :return: True if the node should be used as a chunk else False
        """
        for node_type in PythonChunker.IGNORED_NODES:
            if isinstance(node, node_type):
                return False
        return isinstance(node, ast.stmt)

    @staticmethod
    def _replace_white_space_with_tab(orig_str: str) -> str:
        """
        Replaces the multiple occurrences of white space at the start of the string with the tab character
        :param orig_str:
        :return:
        """
        needs_tab = re.match('^[ ]{2,}', orig_str)
        if needs_tab:
            num_spaces = needs_tab.regs[0][1] - needs_tab.regs[0][0]
            tabs = '\t' * math.floor(num_spaces/PythonChunker.N_SPACE_TO_TAB)
            return re.sub(r'^[ ]{2,}', tabs, orig_str)
        return orig_str
