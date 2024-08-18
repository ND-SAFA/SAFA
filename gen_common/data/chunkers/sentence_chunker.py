from typing import List

from gen_common.data.chunkers.abstract_chunker import AbstractChunker
from gen_common.data.objects.artifact import Artifact
from gen_common.util.str_util import StrUtil


class SentenceChunker(AbstractChunker):

    def chunk(self, artifacts2chunk: List[Artifact]) -> List[List[str]]:
        """
        Chunk artifacts into smaller chunks based on the sentence breaks.
        :param artifacts2chunk: The artifacts to chunk.
        :return: List of the chunks.
        """
        chunks = [StrUtil.split_by_punctuation(Artifact.get_summary_or_content(a)) for a in artifacts2chunk]
        return chunks
