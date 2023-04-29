import os
from typing import List

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker
import ast
import javalang
import javalang.ast

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
        tree

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
    content = FileUtil.read_file("/home/kat/git-repos/safa/tgen/tgen/testres/data/chunker/test_java.java")
    chunker.chunk(content)
