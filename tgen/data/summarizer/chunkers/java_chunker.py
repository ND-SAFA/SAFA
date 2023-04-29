import os
from typing import Dict, List

import javalang
import javalang.ast
from javalang.tree import ClassDeclaration, MethodDeclaration

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker
from tgen.util.file_util import FileUtil


class JavaChunker(AbstractChunker):
    """
    Handles chunking JAVA code into chunks within a model's token limit
    """

    def chunk(self, content: str, id_: str = None) -> List[str]:
        """
        Chunks the given JAVA code into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :param id_: The id_ associated with some content
        :return: The content chunked into sizes beneath the token limit
        """
        lines = content.split(NEW_LINE)
        tree = javalang.parse.parse(content)
        ast_store = {}
        for child in tree.children:
            if isinstance(child, list):
                for class_child in child:
                    definition = self.create_definition(class_child)
                    ast_store[class_child.name] = definition

    @classmethod
    def create_definition(cls, declaration) -> Dict:
        if isinstance(declaration, ClassDeclaration):
            definition = cls.create_children_definition(declaration)
            return definition
        elif isinstance(declaration, MethodDeclaration):
            definition = cls.create_children_definition(declaration)
            definition.pop("children")  # Ignores method body because chunking is no longer optimized past this point.
            return definition
        elif hasattr(declaration, "position"):
            position = declaration.position.line
            return {"start": position, "end": position, "type": JavaChunker.get_declaration_type(declaration)}
        else:
            return {"start": -1, "end": -1, "type": "UNKNOWN"}

    @classmethod
    def create_children_definition(cls, parent_declaration) -> Dict:
        children = [cls.create_definition(c) for c in parent_declaration.body]
        children_positions = [c["end"] for c in children]
        start = parent_declaration.position.line
        end = max(children_positions) + 1 if len(children_positions) > 0 else start
        return {"start": start, "end": end, "children": children, "type": JavaChunker.get_declaration_type(parent_declaration)}

    @staticmethod
    def get_declaration_type(declaration):
        return declaration.__class__.__name__

    @staticmethod
    def _get_node_content(node, lines: List[str]) -> str:
        """
        Gets the content of the node
        :param node: The ast parsed node
        :param lines: The lines of the code file
        :return: The content of the node
        """
        start_lineno = node.lineno - 1
        end_lineno = node.end_lineno
        return os.linesep.join(lines[start_lineno:end_lineno])


if __name__ == "__main__":
    chunker = JavaChunker("model")
    content = FileUtil.read_file("/Users/albertorodriguez/Projects/SAFA/tgen/tgen/testres/data/chunker/test_java.java")
    chunker.chunk(content)
