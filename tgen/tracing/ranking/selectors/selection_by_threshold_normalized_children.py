import pandas as pd
from typing import Dict, List, Tuple

from tgen.common.objects.trace import Trace
from tgen.common.util.math_util import MathUtil
from tgen.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.selectors.i_selection_method import iSelector
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold


class SelectByThresholdNormalizedChildren(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], threshold: float, threshold_based_on_dist: bool = False, min_score: float = None,
               **kwargs) -> List[Trace]:
        """
        Filters the candidate links based on score threshold after score are normalized based on min and max for parent
        :param candidate_entries: Candidate trace entries
        :param threshold: The threshold to filter by
        :param threshold_based_on_dist: If True, calculates a threshold based on the distribution of the data.
        :param min_score: The minimum score in the range (uses the minimum child score if none if provided.
        :return: filtered list of entries
        """
        parent2children, parent2scores = SelectByThresholdNormalizedChildren.group_by_parent(candidate_entries)
        return SelectByThresholdNormalizedChildren._normalized_scores_based_on_parent(parent2children, parent2scores,
                                                                                      threshold=threshold,
                                                                                      min_score=min_score,
                                                                                      threshold_based_on_dist=threshold_based_on_dist)

    @staticmethod
    def _normalized_scores_based_on_parent(parent2children: Dict[str, List[Trace]],
                                           parent2scores: Dict[str, List[float]],
                                           threshold: float,
                                           min_score: float = None,
                                           threshold_based_on_dist: bool = False) -> List[Trace]:
        """
        Normalizes all scores based on the min and max of the parent
        :param parent2children: A dictionary mapping parent id to list of children entries
        :param parent2scores: A dictionary mapping parent id to list of score assigned to children
        :param threshold: The maximum threshold allowed.
        :param min_score: The minimum score in the range (uses the minimum child score if none if provided.
        :param threshold_based_on_dist: If True, calculates a threshold based on the distribution of the data.
        :return: None
        """
        selected_entries = []
        new_threshold = threshold
        for parent, children in parent2children.items():
            sorted_scores = sorted(parent2scores[parent])
            min_child_score = sorted_scores[0] if min_score is None else min_score
            max_child_score = sorted_scores[-1]
            for entry in children:
                score = MathUtil.convert_to_new_range(entry[TraceKeys.SCORE], (min_child_score, max_child_score), (0, 1))
                entry[TraceKeys.SCORE] = score
            if threshold_based_on_dist:
                new_threshold = 1 - (0.5 * pd.Series(RankingUtil.get_scores(children)).std())
                new_threshold = min(new_threshold, threshold)
            selected_entries.extend(SelectByThreshold.select(children, new_threshold))
        return selected_entries

    @staticmethod
    def group_by_parent(candidate_entries: List[Trace]) -> Tuple[Dict[str, List[Trace]], Dict[str, List[float]]]:
        """
        Groups entries and scores by the parent artifact
        :param candidate_entries: :param candidate_entries: Candidate trace entries
        :return: A dictionary mapping parent id to list of children entries and mapping id to list of scores assigned to children
        """
        parent2children = {}
        parent2scores = {}
        for entry in candidate_entries:
            parent = entry[TraceKeys.parent_label()]
            if parent not in parent2children:
                parent2children[parent] = []
                parent2scores[parent] = []
            parent2children[parent].append(entry)
            parent2scores[parent].append(entry[TraceKeys.SCORE])
        return parent2children, parent2scores
