from typing import Dict, List, Tuple

from tgen.common.objects.trace import Trace
from tgen.common.util.math_util import MathUtil
from tgen.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.selectors.i_selection_method import iSelector
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold


class SelectByThresholdScaledAcrossAll(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], threshold: float, **kwargs) -> List[Trace]:
        """
        Filters the candidate links based on score threshold after score are normalized based on min and max for parent
        :param candidate_entries: Candidate trace entries
        :param threshold: The threshold to filter by
        :return: filtered list of entries
        """
        SelectByThresholdScaledAcrossAll._normalized_scores_based_on_parent(candidate_entries)
        return SelectByThreshold.select(candidate_entries, threshold)

    @staticmethod
    def _normalized_scores_based_on_parent(candidate_entries: List[Trace]) -> None:
        """
        Normalizes all scores based on the min and max of all scores
        :param candidate_entries: Candidate trace entries
        :return: None
        """
        scores = [e[TraceKeys.SCORE] for e in candidate_entries]
        min_score, max_score = min(scores), max(scores)
        for entry in candidate_entries:
            entry[TraceKeys.SCORE] = MathUtil.convert_to_new_range(entry[TraceKeys.SCORE], (0, max_score), (0, 1))