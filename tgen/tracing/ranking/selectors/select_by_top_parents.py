from trace import Trace
from typing import List

from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.selectors.i_selection_method import iSelector


class SelectByTopParents(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], **kwargs) -> List[Trace]:
        """
        Filters the candidate links based tiers where highly related parents are prioritized but at least one parent is selected always
        :param candidate_entries: Candidate trace entries
        :return: filtered list of entries
        """
        return RankingUtil.select_predictions(candidate_entries)