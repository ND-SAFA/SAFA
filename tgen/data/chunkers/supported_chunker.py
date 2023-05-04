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
        ext = FileUtil.get_file_ext(path_to_file)
        try:
            return SupportedChunker[ext[1:].upper()]
        except Exception:
            return default
