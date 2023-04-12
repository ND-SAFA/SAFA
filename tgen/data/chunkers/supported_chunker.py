from tgen.data.chunkers.java_chunker import JavaChunker
from tgen.data.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.chunkers.python_chunker import PythonChunker


class SupportedChunker:
    PY = PythonChunker
    JAVA = JavaChunker
    NL = NaturalLanguageChunker