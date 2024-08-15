from typing import List, Type

import javalang
import javalang.ast
from common_resources.tools.constants.symbol_constants import BRACKET_CLOSE, BRACKET_OPEN, NEW_LINE, SEMI_COLON
from javalang import tree as javatree
from javalang.tree import Declaration, Import, PackageDeclaration

from tgen.data.chunkers.token_limit_chunkers.abstract_code_chunker import AbstractCodeChunker
from tgen.data.chunkers.token_limit_chunkers.chunked_node import ChunkedNode


class UnknownNode:
    pass


class JavaChunker(AbstractCodeChunker):
    """
    Handles chunking JAVA code into chunks within a model's token limit
    """

    COMMENT_START = "/*"
    IGNORED_NODES = [UnknownNode, Import, PackageDeclaration]

    @staticmethod
    def _parse(content: str, id_: str = None) -> ChunkedNode:
        """
        Chunks the given JAVA code into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :param id_: The id_ associated with some content
        :return: The content chunked into sizes beneath the token limit
        """
        lines = content.split(NEW_LINE)
        tree = javalang.parse.parse(content)
        top_level_classes = [JavaChunker._create_chunked_node(class_child, lines) for child in tree.children
                             if isinstance(child, list) for class_child in child]
        return ChunkedNode(lineno=min([c.lineno for c in top_level_classes]),
                           end_lineno=max([c.end_lineno for c in top_level_classes]) + 1,
                           body=top_level_classes, type=ChunkedNode.get_type_name(tree))

    @staticmethod
    def _create_chunked_node(java_node: javatree.Node, lines: List[str]) -> ChunkedNode:
        """
        Creates a node from the parsed syntax java
        :param java_node: The java_node object for classes, methods, statements, ect.
        :param lines: The lines of the original file
        :return: The node for chunking
        """
        children = JavaChunker._get_children(java_node)
        if len(children) > 0 or hasattr(java_node, "body"):
            return JavaChunker._create_node_with_children(java_node, lines, children=children)
        elif JavaChunker._has_position(java_node):
            return JavaChunker._create_chunked_node_without_children(java_node, lines)
        else:
            return ChunkedNode(lineno=-1, end_lineno=-1, type=UnknownNode.__name__)

    @staticmethod
    def _create_chunked_node_without_children(java_node: javatree.Node, lines: List[str]) -> ChunkedNode:
        """
        Creates a single node without children from the parsed syntax tree
        :param java_node: The java node object that has no children
        :param lines: The lines of the original file
        :return: The node for chunking
        """
        position = JavaChunker._get_position_start_lineno(java_node, lines)
        end_lineno = JavaChunker._get_single_node_endlineno(position, lines)
        return ChunkedNode(lineno=position, end_lineno=end_lineno, type=ChunkedNode.get_type_name(java_node))

    @staticmethod
    def _create_node_with_children(parent_java_node: javatree.Node, lines: List[str], children: List) -> ChunkedNode:
        """
        Creates a node that has children (body) from the parsed syntax tree
        :param parent_java_node: The parent java node object for classes, methods, and other nodes with children
        :param lines: The lines of the original file
        :param children: The children of the node.
        :return: The node for chunking
        """
        children_nodes = [JavaChunker._create_chunked_node(c, lines) for c in children]
        children_nodes = [child for child in children_nodes if JavaChunker._is_node_2_use(child)]
        children_end_linenos = [c.end_lineno for c in children_nodes]
        start = JavaChunker._get_position_start_lineno(parent_java_node, lines)
        end = JavaChunker._get_parent_node_end_lineno(parent_java_node, children_end_linenos, lines)
        return ChunkedNode(lineno=start, end_lineno=end, body=children_nodes, type=ChunkedNode.get_type_name(parent_java_node))

    @staticmethod
    def _get_children(parent_java_node: javatree.Node) -> List[javatree.Node]:
        """
        Gets all relevant children that belong to the parent
        :param parent_java_node: The parent node
        :return: The list of all relevant children that belong to the parent
        """
        if hasattr(parent_java_node, "body"):
            children = parent_java_node.body if parent_java_node.body is not None else []
            if not isinstance(children, list):
                children = JavaChunker._filter_irrelevant_children(children, children.children) if hasattr(children, "children") \
                    else [children]
            return children
        elif hasattr(parent_java_node, "children") and (JavaChunker._has_position(parent_java_node)):
            return JavaChunker._filter_irrelevant_children(parent_java_node, parent_java_node.children)
        else:
            return []

    @staticmethod
    def _filter_irrelevant_children(parent_java_node: javatree.Node, all_children: List[javatree.Node]) -> List[
        javatree.Node]:
        """
        Removes all the children that don't represent chunked nodes that are included in the javalang parser for unknown reasons
        :param parent_java_node: The parent node
        :param all_children: All its children (unfiltered)
        :return: Only the relevant children (filtered)
        """
        relevant_children = []
        for child in all_children:
            if isinstance(child, list):
                all_children.extend(JavaChunker._filter_irrelevant_children(parent_java_node, child))
            elif JavaChunker._has_position(child):
                relevant_children.append(child)
        return relevant_children

    @staticmethod
    def _get_position_start_lineno(java_node: Declaration, lines: List[str]) -> int:
        """
        Gets the start lineno from the java_node position
        :param java_node: The java_node object for classes, methods, statements, ect.
        :param lines: The lines of the java node.
        :return: The start lineno from the java_node position
        """
        start = java_node.position.line - 1  # index starting at 0
        if getattr(java_node, "documentation", None):
            for i in range(1, start):
                if lines[start - i].strip().startswith(JavaChunker.COMMENT_START):
                    start = start - i
                    break
        elif getattr(java_node, "annotations", []):
            start = start - len(java_node.annotations)
        return start

    @staticmethod
    def _get_parent_node_end_lineno(parent_java_node: javatree.Node, children_end_linenos: List[int], lines: List[str]) -> int:
        """
        Gets the end lineno of the java_node with children
        :param parent_java_node: The parent node to get end line number for
        :param children_end_linenos: The list of end positions of all children
        :param lines: The lines from the code file
        :return: The end lineno of the node
        """
        start = parent_java_node.position.line - 1
        end = start + 1
        if len(children_end_linenos) > 0 and max(children_end_linenos) != start + 1:
            end = max(children_end_linenos)  # parent end should go to at least the end of the last child
        if BRACKET_OPEN in lines[start] and BRACKET_CLOSE not in lines[end]:
            return JavaChunker._find_line_with_sym(BRACKET_CLOSE, end, lines)
        return end

    @staticmethod
    def _get_single_node_endlineno(start_lineno: int, lines: List[str]) -> int:
        """
        Gets the end lineno of the java_node without children
        :param start_lineno: The starting line of the java_node
        :param lines: The lines from the code file
        :return: The end lineno for the java_node
        """
        return JavaChunker._find_line_with_sym(SEMI_COLON, start_lineno, lines)

    @staticmethod
    def _find_line_with_sym(sym2find: str, start: int, lines: List[str]) -> int:
        """
        Finds the first line number after or at the start line that contains the given symbol
        :param sym2find: The symbol to find
        :param start: The line number to start at
        :param lines: All lines of the code file
        :return: The line number containing the symbol
        """
        lineno = start
        for i, line in enumerate(lines[start:]):
            if sym2find in line:
                lineno = start + i
                break
        return lineno

    @staticmethod
    def _has_position(java_node: javatree.Node) -> bool:
        """
        Returns True if the given node has a position, else False
        :param java_node: The node
        :return: True if the given node has a position, else False
        """
        return getattr(java_node, "position", None) is not None

    @staticmethod
    def _preprocess_line(line: str) -> str:
        """
        Strips the extra spaces from the line
        :param line: The original line
        :return: The processed line
        """
        return line.strip()

    @staticmethod
    def _get_ignored_nodes() -> List[Type]:
        """
        Returns a list of node types that are NOT part of the hierarchy used for chunking
        :return: The list of node types not used as chunks
        """
        return JavaChunker.IGNORED_NODES
