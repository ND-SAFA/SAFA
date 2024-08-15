from typing import List

from common_resources.data.objects.trace import Trace
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.trace_selectors.i_selection_method import iSelector


class SelectByThreshold(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], threshold: float, **kwargs) -> List[Trace]:
        """
        Filters the candidate links based on score threshold
        :param candidate_entries: Candidate trace entries
        :param threshold: The threshold to filter by
        :return: filtered list of entries
        """
        return RankingUtil.select_traces_by_threshold(candidate_entries, threshold)
