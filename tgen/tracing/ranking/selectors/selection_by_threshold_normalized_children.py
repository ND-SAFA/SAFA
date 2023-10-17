from typing import List, Tuple, Dict

from tgen.common.objects.trace import Trace
from tgen.common.util.math_util import MathUtil
from tgen.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.selectors.i_selection_method import iSelector
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold


class SelectByThresholdNormalizedChildren(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], threshold: float, **kwargs) -> List[Trace]:
        """
        Filters the candidate links based on score threshold after score are normalized based on min and max for parent
        :param candidate_entries: Candidate trace entries
        :param threshold: The threshold to filter by
        :return: filtered list of entries
        """
        parent2children, parent2scores = SelectByThresholdNormalizedChildren._group_by_parent(candidate_entries)
        SelectByThresholdNormalizedChildren._normalized_scores_based_on_parent(parent2children, parent2scores)
        return SelectByThreshold.select(candidate_entries, threshold)

    @staticmethod
    def _normalized_scores_based_on_parent(parent2children: Dict[str, List[Trace]], parent2scores: Dict[str, List[float]]) -> None:
        """
        Normalizes all scores based on the min and max of the parent
        :param parent2children: A dictionary mapping parent id to list of children entries
        :param parent2scores: A dictionary mapping parent id to list of score assigned to children
        :return: None
        """
        for parent, children in parent2children.items():
            sorted_scores = sorted(parent2scores[parent])
            min_score, max_score = sorted_scores[0], sorted_scores[-1]
            for entry in children:
                entry[TraceKeys.SCORE] = MathUtil.convert_to_new_range(entry[TraceKeys.SCORE], (min_score, max_score), (0, 1))

    @staticmethod
    def _group_by_parent(candidate_entries: List[Trace]) -> Tuple[Dict[str, List[Trace]], Dict[str, List[float]]]:
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
