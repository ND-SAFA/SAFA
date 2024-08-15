from copy import deepcopy
from typing import List

from common_resources.tools.constants.symbol_constants import SPACE

from tgen.data.chunkers.token_limit_chunkers.abstract_token_limit_chunker import AbstractTokenLimitChunker
from tgen.models.tokens.token_calculator import TokenCalculator


class NaturalLanguageChunker(AbstractTokenLimitChunker):
    """
    Handles chunking NL text into chunks within a model's token limit
    """

    def chunk(self, content: str, id_: str = None) -> List[str]:
        """
        Chunks the given natural language content into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :param id_: The id_ associated with the content
        :return: The content chunked into sizes beneath the token limit
        """
        if not self.exceeds_token_limit(content):
            return [content]
        chunks, new_chunk = [], []
        n_tokens_for_chunk = 0
        for word in content.split():
            n_tokens_for_chunk += TokenCalculator.estimate_num_tokens(word, self.model_name)
            if n_tokens_for_chunk > self.max_prompt_tokens:
                chunks.append(deepcopy(new_chunk))
                new_chunk = [word]
                n_tokens_for_chunk = TokenCalculator.estimate_num_tokens(word, self.model_name)
            else:
                new_chunk.append(word)
        if len(new_chunk) > 0:
            chunks.append(new_chunk)
        return [SPACE.join(words) for words in chunks]
