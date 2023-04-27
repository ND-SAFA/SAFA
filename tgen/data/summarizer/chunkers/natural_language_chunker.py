from typing import List

from tgen.constants.deliminator_constants import SPACE
from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker


class NaturalLanguageChunker(AbstractChunker):
    """
    Handles chunking NL text into chunks within a model's token limit
    """

    def chunk(self, content: str) -> List[str]:
        """
        Chunks the given natural language content into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :return: The content chunked into sizes beneath the token limit
        """
        if not self.exceeds_token_limit(content):
            return [content]
        n_words_per_chunk = self.estimate_num_words_from_tokens(self.token_limit)
        words = content.split()
        return [SPACE.join(words[i:i + n_words_per_chunk]) for i in range(0, len(words), n_words_per_chunk)]
