import ast
import math
import os
import re
from typing import List, Union, Tuple

import tiktoken

from tgen.constants.deliminator_constants import TAB
from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker
from tgen.data.summarizer.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.util.logging.logger_manager import logger
from tgen.util.override import overrides

Node = Union[ast.AST, ast.stmt]


class PythonChunker(AbstractChunker):
    """
    Handles chunking Python code into chunks within a model's token limit
    """

    IGNORED_NODES = [ast.Import, ast.ImportFrom]
    N_SPACE_TO_TAB = 4

    def chunk(self, content: str, id_: str = None) -> List[str]:
        """
        Chunks the given python code into pieces that are beneath the model's token limit
        :param content: The code to be chunked
        :param id_: The id associated with the content to summarize
        :return: The nodes chunked into sizes beneath the token limit
        """
        lines = [self._replace_white_space_with_tab(line) for line in content.split(os.linesep)]
        try:
            nodes = ast.parse(content)
        except Exception:
            msg_end = id_ if id_ else f"starting with {lines[0]}"
            logger.warning(f"Unable to parse file {msg_end}")
            return NaturalLanguageChunker(model_name=self.model_name).chunk(content)
        chunks = self.__chunk_helper(nodes, lines)
        return [self._get_node_content(chunk, lines) for chunk in chunks if abs(chunk.lineno - chunk.end_lineno) >= 1]

    def __chunk_helper(self, p_node: Node, lines: List[str]) -> List[Node]:
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
                if not hasattr(chunk, "body"):
                    chunks.append(self._resize_node(chunk, lines))
                else:
                    new_chunks = self.__chunk_helper(chunk, lines)
                    chunk.end_lineno = new_chunks[0].lineno - 1  # ensure no content from parent is lost
                    chunk, child_chunks = self.maximize_chunk_content_length(chunk, new_chunks, lines)
                    chunks.extend([chunk] + child_chunks)
            else:
                chunks.append(chunk)
        if len(chunks) > 1:
            chunk, child_chunks = self.maximize_chunk_content_length(chunks[0], chunks[1:], lines)
            chunks = [chunk] + child_chunks
        return chunks

    def maximize_chunk_content_length(self, p_chunk: Node, child_chunks: List[Node], lines: List[str]) -> Tuple[Node, List[Node]]:
        """
        Combines all children chunk so long as the combined tokens are beneath the token limit
        :param p_chunk: Parent chunk
        :param lines: Lines from the code file
        :param child_chunks: The new, children chunks
        :return: The new parent chunk containing the maximum number of children and a list of any remaining children
        """
        parent_tokens = self.estimate_num_tokens(self._get_node_content(p_chunk, lines), self.model_name)
        for i in range(len(child_chunks)):
            child = child_chunks[i]
            c_tokens = self.estimate_num_tokens(self._get_node_content(child, lines), self.model_name)
            if c_tokens + parent_tokens > self.token_limit:
                break
            p_chunk.end_lineno = child.end_lineno
            parent_tokens += c_tokens
        if i + 1 < len(child_chunks):
            new_parent, new_children = self.maximize_chunk_content_length(child_chunks[i], child_chunks[i + 1:], lines)
            child_chunks = [new_parent] + new_children
        else:
            child_chunks = child_chunks[i:]
        return p_chunk, child_chunks

    @staticmethod
    @overrides(AbstractChunker)
    def estimate_num_tokens(content: Union[Node, str], model_name: str) -> int:
        """
        Approximates the number of tokens that some content will be tokenized into by a given model.
        :param content: The content to be tokenized
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(content))
        return num_tokens

    def _resize_node(self, node: Node, lines: List[str]) -> Node:
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
    def _get_node_content(node: Node, lines: List[str]) -> str:
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
    def _node2use(node: Node) -> bool:
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
            tabs = TAB * math.floor(num_spaces / PythonChunker.N_SPACE_TO_TAB)
            return re.sub(r'^[ ]{2,}', tabs, orig_str)
        return orig_str
