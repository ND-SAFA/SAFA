from trace import Trace
from typing import List, Tuple

from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.trace_selectors.i_selection_method import iSelector


class SelectByTopParents(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], parent_thresholds: Tuple[float, float, float], **kwargs) -> List[Trace]:
        """
        Filters the candidate links based tiers where highly related parents are prioritized but at least one parent is selected always
        :param candidate_entries: Candidate trace entries
        :param parent_thresholds: The threshold used to establish parents from (primary, secondary and min)
        :return: filtered list of entries
        """
        return RankingUtil.select_predictions_by_thresholds(candidate_entries, primary_threshold=parent_thresholds[0],
                                                            secondary_threshold=parent_thresholds[1],
                                                            min_threshold=parent_thresholds[2])
