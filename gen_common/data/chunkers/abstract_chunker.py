from abc import abstractmethod, ABC

from typing import List

from gen_common.data.objects.artifact import Artifact


class AbstractChunker(ABC):

    @abstractmethod
    def chunk(self, artifacts2chunk: List[Artifact]) -> List[List[str]]:
        """
        Breaks artifacts into smaller chunks.
        :param artifacts2chunk: The artifacts to chunk.
        :return: List of the chunks.
        """
