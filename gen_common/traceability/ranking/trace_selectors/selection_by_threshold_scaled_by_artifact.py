from typing import List

from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.data.objects.trace import Trace
from gen_common.traceability.ranking.trace_selectors.i_selection_method import iSelector
from gen_common.util.ranking_util import RankingUtil


class SelectByThresholdScaledByArtifacts(iSelector):

    @staticmethod
    def select(candidate_entries: List[Trace], threshold: float, threshold_based_on_dist: bool = False,
               min_score: float = None, artifact_type: str = TraceKeys.child_label(), **kwargs) -> List[Trace]:
        """
        Filters the candidate links based on score threshold after score are normalized based on min and max for parent
        :param candidate_entries: Candidate trace entries
        :param threshold: The threshold to filter by
        :param threshold_based_on_dist: If True, calculates a threshold based on the distribution of the data.
        :param min_score: The minimum score in the range (uses the minimum child score if none if provided.
        :param artifact_type: The type of artifact (parent or child) to normalize by.
        :return: filtered list of entries
        """
        artifact2traces = RankingUtil.group_trace_predictions(candidate_entries, artifact_type)
        RankingUtil.normalized_scores_by_individual_artifacts(artifact2traces, min_score)
        return RankingUtil.select_traces_by_artifact(artifact2traces,
                                                     threshold=threshold,
                                                     threshold_based_on_dist=threshold_based_on_dist)
