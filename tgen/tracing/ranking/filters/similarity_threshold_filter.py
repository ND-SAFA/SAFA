from copy import deepcopy
from typing import Dict, List

from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.list_util import ListUtil
from common_resources.tools.util.np_util import NpUtil
from common_resources.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.filters.i_filter import iFilter


class SimilarityThresholdFilter(iFilter):

    @staticmethod
    def filter(parent2children: Dict[str, List[EnumDict]], children_ids: List[str], parent_ids: List[str],
               **kwargs) -> Dict[str, List]:
        """
        Filters the children artifacts based on how similarity they are to the parent compared to all parents.
        :param parent2children: Maps parent id to a list of its children ids and a list of their associated scores.
        :param children_ids: List of ids of each child artifact.
        :param parent_ids: List of ids of each parent artifact.
        :return: Map of parent to list of sorted children traces with non-selected children scores set to 0.
        """
        threshold_scores = SimilarityThresholdFilter._find_thresholds_for_artifacts(parent2children)

        parent2children_filtered = {}
        for p_id, traces in parent2children.items():
            updated_traces = SimilarityThresholdFilter._update_scores(traces, threshold_scores,
                                                                      children_ids, parent_ids)
            parent2children_filtered[p_id] = updated_traces
        return parent2children_filtered

    @staticmethod
    def _find_thresholds_for_artifacts(parent2children: Dict[str, List[EnumDict]]) -> Dict[str, float]:
        """
        Finds a threshold for each child artifact, above which that artifact will be selected for a parent.
        :param parent2children: Maps parent id to a list of children and associated scores.
        :return: A mapping of child artifact to its threshold.
        """
        total_scores = {}
        for traces in parent2children.values():
            for trace in traces:
                child, score = trace[TraceKeys.child_label()], trace[TraceKeys.SCORE]
                DictUtil.set_or_append_item(total_scores, child, score)
        threshold_scores = {c_id: NpUtil.detect_outlier_scores(scores, sigma=1, ensure_at_least_one_detection=True)[1]
                            for c_id, scores in total_scores.items()}
        return threshold_scores

    @staticmethod
    def _update_scores(traces: List[EnumDict], threshold_scores: Dict[str, float],
                       children_ids: List[str], parent_ids: List[str]) -> List[EnumDict]:
        """
        Sets any scores that do not match the threshold for a child to 0.
        :param traces: List of traces for a parent.
        :param threshold_scores:  A mapping of child artifact to its threshold.
        :param children_ids: List of ids of each child artifact.
        :param parent_ids: List of ids of each parent artifact (place holder for now).
        :return: A list of the selected traces for the children where scores below the threshold are set to 0.
        """
        updated_traces = []
        for trace in traces:
            c_id, score = trace[TraceKeys.child_label()], trace[TraceKeys.SCORE]
            updated_trace = deepcopy(trace)
            new_score = score if threshold_scores[c_id] <= score else 0
            updated_trace[TraceKeys.SCORE] = new_score
            updated_traces.append(updated_trace)
        SimilarityThresholdFilter._ensure_at_least_one_trace_per_parent(traces, updated_traces, children_ids)
        return updated_traces

    @staticmethod
    def _ensure_at_least_one_trace_per_parent(traces: List[EnumDict], updated_traces: List[EnumDict], children_ids: List[str]) -> None:
        """
        Ensures that each parent has at least one child that was not filtered.
        :param traces: List of all original traces.
        :param updated_traces: List of updated traces.
        :param children_ids: Ids of the possible children.
        :return: None (updates directly)
        """
        indices_full_text = [i for i, trace in enumerate(updated_traces) if trace[TraceKeys.SOURCE] in children_ids]
        indices_chunks = list(set(range(len(traces))).difference(indices_full_text))
        for indices in [indices_full_text, indices_chunks]:
            if not indices:
                continue
            updated_traces_subset = [updated_traces[i] for i in indices]
            if not any(RankingUtil.get_scores(updated_traces_subset)):
                original_traces_subset = [traces[i] for i in indices]
                top_trace_loc, _ = ListUtil.get_max_value_with_index(RankingUtil.get_scores(original_traces_subset))
                orig_index_of_top_trace = indices[top_trace_loc]
                updated_traces[orig_index_of_top_trace] = traces[orig_index_of_top_trace]
