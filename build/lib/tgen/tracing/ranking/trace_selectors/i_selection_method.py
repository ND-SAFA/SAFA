from abc import abstractmethod
from typing import List

from common_resources.data.objects.trace import Trace


class iSelector:

    @staticmethod
    @abstractmethod
    def select(candidate_entries: List[Trace], **kwargs) -> List[Trace]:
        """
        Filters the candidate links
        :param candidate_entries: Candidate trace entries
        :return: filtered list of entries
        """
        pass
