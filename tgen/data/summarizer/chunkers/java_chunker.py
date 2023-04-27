from typing import List

from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker


class JavaChunker(AbstractChunker):
    """
    Handles chunking JAVA code into chunks within a model's token limit
    """

    def chunk(self, content: str) -> List[str]:
        """
        Chunks the given JAVA code into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :return: The content chunked into sizes beneath the token limit
        """
        # TODO
        raise NotImplementedError()
