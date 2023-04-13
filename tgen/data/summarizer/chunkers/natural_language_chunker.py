from typing import List

from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker


class NaturalLanguageChunker(AbstractChunker):
    """
    Handles chunking NL text into chunks within a model's token limit
    """

    def _chunk(self, content: str) -> List[str]:
        """
        Chunks the given natural language content into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :return: The content chunked into sizes beneath the token limit
        """
        return [content]
        # TODO
        raise NotImplementedError()
