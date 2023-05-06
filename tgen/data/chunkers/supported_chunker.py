from enum import Enum

from tgen.data.chunkers.java_chunker import JavaChunker
from tgen.data.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.util.file_util import FileUtil
from tgen.util.supported_enum import SupportedEnum


class SupportedChunker(SupportedEnum):
    PY = PythonChunker
    JAVA = JavaChunker
    NL = NaturalLanguageChunker

    @staticmethod
    def determine_from_path(path_to_file: str = None) -> "SupportedChunker":
        """
        Gets the chunker responsible for breaking a file or content into smaller pieces for the model
        :param path_to_file: The path to the file being chunked
        :return: The chunker to use
        """
        default = SupportedChunker.NL
        if not path_to_file:
            return default
        ext = FileUtil.get_file_ext(path_to_file).split(".")[-1]
        return SupportedChunker.get_chunker_from_ext(ext)

    @staticmethod
    def get_chunker_from_ext(ext: str) -> "SupportedChunker":
        """
        Gets the chunker responsible for breaking content into smaller pieces for the model
        :param ext: The ext of the file being chunked
        :return: The chunker to use
        """
        try:
            return SupportedChunker[ext.upper()]
        except KeyError:
            return SupportedChunker.NL
