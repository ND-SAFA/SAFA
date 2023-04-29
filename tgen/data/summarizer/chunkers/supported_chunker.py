from enum import Enum

from tgen.data.summarizer.chunkers.java_chunker import JavaChunker
from tgen.data.summarizer.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.summarizer.chunkers.python_chunker import PythonChunker
from tgen.util.supported_enum import SupportedEnum


class SupportedChunker(SupportedEnum):
    PY = PythonChunker
    JAVA = JavaChunker
    NL = NaturalLanguageChunker
