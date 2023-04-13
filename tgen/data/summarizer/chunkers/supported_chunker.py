from tgen.data.summarizers.chunkers.java_chunker import JavaChunker
from tgen.data.summarizers.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.summarizers.chunkers.python_chunker import PythonChunker


class SupportedChunker:
    PY = PythonChunker
    JAVA = JavaChunker
    NL = NaturalLanguageChunker