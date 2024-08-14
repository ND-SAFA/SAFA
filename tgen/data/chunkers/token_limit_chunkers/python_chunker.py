import ast
import math
import re
from copy import deepcopy
from typing import List, Type, Union

from common_resources.tools.constants.symbol_constants import TAB

from common_resources.tools.util.override import overrides
from tgen.data.chunkers.token_limit_chunkers.abstract_code_chunker import AbstractCodeChunker
from tgen.data.chunkers.token_limit_chunkers.chunked_node import ChunkedNode

ASTNode = Union[ast.AST, ast.stmt]


class PythonChunker(AbstractCodeChunker):
    """
    Handles chunking Python code into chunks within a model's token limit
    """

    IGNORED_NODES = [ast.Import, ast.ImportFrom]
    N_SPACE_TO_TAB = 4

    @staticmethod
    def _parse(content: str) -> ChunkedNode:
        """
        Parses the content into Python ast, converts to Nodes and returns the head node
        :param content: The code content
        :return: The head node
        """
        nodes = ast.parse(content)
        if len(nodes.body) == 0:
            line_start = 0
            line_end = len(content.splitlines())
            return ChunkedNode(lineno=line_start,
                               end_lineno=line_end,
                               type="",
                               body=[ChunkedNode(
                                   lineno=line_start,
                                   end_lineno=line_end,
                                   type="",
                                   body=[]
                               )])
        return ChunkedNode.from_python_ast(nodes)

    @staticmethod
    @overrides(AbstractCodeChunker)
    def _get_node_content(node: ChunkedNode, lines: List[str]) -> str:
        """
        Gets the content of the node
        :param node: The ast parsed node
        :param lines: The lines of the code file
        :return: The content of the node
        """
        node_copy = deepcopy(node)
        node_copy.lineno = node.lineno - 1  # python ast leaves out the class/function definition in lineno
        node_copy.end_lineno = node.end_lineno - 1
        content = AbstractCodeChunker._get_node_content(node_copy, lines)
        return content

    @staticmethod
    def _get_ignored_nodes() -> List[Type]:
        """
        Returns a list of node types that are NOT part of the hierarchy used for chunking
        :return: The list of node types not used as chunks
        """
        return PythonChunker.IGNORED_NODES

    @staticmethod
    def _preprocess_line(line: str) -> str:
        """
        Replaces the multiple occurrences of white space at the start of the string with the tab character
        :param line: The original line
        :return: The processed line
        """
        needs_tab = re.match('^[ ]{2,}', line)
        if needs_tab:
            num_spaces = needs_tab.regs[0][1] - needs_tab.regs[0][0]
            tabs = TAB * math.floor(num_spaces / PythonChunker.N_SPACE_TO_TAB)
            return re.sub(r'^[ ]{2,}', tabs, line)
        return line
