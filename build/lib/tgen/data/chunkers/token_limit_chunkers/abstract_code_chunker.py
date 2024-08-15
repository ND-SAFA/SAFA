import os
from abc import ABC, abstractmethod
from asyncio.log import logger
from typing import List, Tuple, Type

from tgen.data.chunkers.token_limit_chunkers.abstract_token_limit_chunker import AbstractTokenLimitChunker
from tgen.data.chunkers.token_limit_chunkers.chunked_node import ChunkedNode
from tgen.data.chunkers.token_limit_chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.models.tokens.token_calculator import TokenCalculator


class AbstractCodeChunker(AbstractTokenLimitChunker, ABC):

    def chunk(self, content: str, id_: str = None) -> List[str]:
        """
        Chunks the given python code into pieces that are beneath the model's token limit
        :param content: The code to be chunked
        :param id_: The id associated with the content to summarize
        :return: The nodes chunked into sizes beneath the token limit
        """
        lines = [self._preprocess_line(line) for line in content.splitlines(keepends=True)]
        try:
            head_node = self._parse(content)
        except Exception as e:
            msg_end = id_ if id_ else f"starting with {lines[0]}"
            logger.warning(f"Unable to parse file {msg_end}")
            return NaturalLanguageChunker(model_name=self.model_name, max_prompt_tokens=self.max_prompt_tokens).chunk(content)
        chunks = self.__chunk_helper(head_node, lines)
        chunk_contents = [self._get_node_content(chunk, lines) for chunk in chunks]
        return chunk_contents

    def __chunk_helper(self, p_node: ChunkedNode, lines: List[str]) -> List[ChunkedNode]:
        """
        Performs the recursive chunking function to obtain chunks that are under the token limit
        :param p_node: The parent node
        :param lines: The lines from the code file
        :return: The nodes chunked into sizes under the token limit
        """
        potential_chunks: List[ChunkedNode] = [node for node in p_node.body if self._is_node_2_use(node)]
        chunks = []
        for chunk in potential_chunks:
            content = self._get_node_content(chunk, lines)
            if self.exceeds_token_limit(content):
                if not chunk.body:
                    chunks.append(self._resize_node(chunk, lines))
                else:
                    new_chunks = self.__chunk_helper(chunk, lines)
                    chunk.end_lineno = new_chunks[0].lineno - 1  # ensure no content from parent is lost
                    chunk, child_chunks = self._maximize_chunk_content_length(chunk, new_chunks, lines)
                    chunks.extend([chunk] + child_chunks)
            else:
                chunks.append(chunk)
        if len(chunks) > 1:
            chunk, child_chunks = self._maximize_chunk_content_length(chunks[0], chunks[1:], lines)
            chunks = [chunk] + child_chunks
        return chunks

    def _maximize_chunk_content_length(self, p_chunk: ChunkedNode, child_chunks: List[ChunkedNode], lines: List[str]) \
            -> Tuple[ChunkedNode, List[ChunkedNode]]:
        """
        Combines all children chunk so long as the combined tokens are beneath the token limit
        :param p_chunk: Parent chunk
        :param lines: Lines from the code file
        :param child_chunks: The new, children chunks
        :return: The new parent chunk containing the maximum number of children and a list of any remaining children
        """
        i = 0
        for child in child_chunks:
            parent_tokens = TokenCalculator.estimate_num_tokens(self._get_node_content(p_chunk, lines), self.model_name)
            c_tokens = TokenCalculator.estimate_num_tokens(self._get_node_content(child, lines), self.model_name)
            if (c_tokens + parent_tokens) > self.max_prompt_tokens:
                break
            p_chunk.end_lineno = child.end_lineno
            p_chunk.body.append(child)
            i += 1
        if i + 1 < len(child_chunks):
            new_parent, new_children = self._maximize_chunk_content_length(child_chunks[i], child_chunks[i + 1:], lines)
            child_chunks = [new_parent] + new_children
        else:
            child_chunks = child_chunks[i:]
        return p_chunk, child_chunks

    @staticmethod
    def _get_node_content(node: ChunkedNode, lines: List[str]) -> str:
        """
        Gets the content of the node
        :param node: The ast parsed node
        :param lines: The lines of the code file
        :return: The content of the node
        """
        start_lineno = node.lineno
        end_lineno = node.end_lineno
        return os.linesep.join(lines[start_lineno:end_lineno + 1])

    def _resize_node(self, node: ChunkedNode, lines: List[str]) -> ChunkedNode:
        """
        Resizes the node to fit within the required number of tokens.
        :param node: The node to resize.
        :param lines: The lines of the code node.
        :return: The resized node
        """
        content = self._get_node_content(node, lines)
        while self.exceeds_token_limit(content):
            content = self._get_node_content(node, lines)
            node.end_lineno -= 1
            if node.end_lineno == node.lineno:
                break
        return node

    @classmethod
    def _is_node_2_use(cls, node: ChunkedNode) -> bool:
        """
        Determines if the node is a part of the hierarchy used for chunking
        :param node: The node
        :return: True if the node should be used as a chunk else False
        """
        for node_type in cls._get_ignored_nodes():
            if node.type == node_type.__name__:
                return False
        return True

    @staticmethod
    @abstractmethod
    def _parse(content: str) -> ChunkedNode:
        """
        Parses the content and returns the head node
        :param content: The code content
        :return: The head node
        """

    @staticmethod
    @abstractmethod
    def _preprocess_line(line: str) -> str:
        """
        Performs any necessary preprocessing on each code file line
        :param line: A line from the code file
        :return: The processed line
        """

    @staticmethod
    @abstractmethod
    def _get_ignored_nodes() -> List[Type]:
        """
        Returns a list of node types that are NOT part of the hierarchy used for chunking
        :return: The list of node types not used as chunks
        """
