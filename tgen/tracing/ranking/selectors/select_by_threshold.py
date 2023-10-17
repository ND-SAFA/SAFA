from typing import List

from tgen.common.objects.trace import Trace
from tgen.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.selectors.i_selection_method import iSelector


class SelectByThreshold(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], threshold: float, **kwargs) -> List[Trace]:
        """
        Filters the candidate links based on score threshold
        :param candidate_entries: Candidate trace entries
        :param threshold: The threshold to filter by
        :return: filtered list of entries
        """
        return [c for c in candidate_entries if TraceKeys.SCORE in c and c[TraceKeys.SCORE] >= threshold]
