from tgen.data.summarizer.chunkers.java_chunker import JavaChunker
from tgen.data.summarizer.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.summarizer.chunkers.python_chunker import PythonChunker


class SupportedChunker:
    PY = PythonChunker
    JAVA = JavaChunker
    NL = NaturalLanguageChunker