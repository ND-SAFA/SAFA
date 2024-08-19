from typing import Dict

from gen_common.constants.ranking_constants import CLUSTERING_LINK_THRESHOLD
from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.common.ranking_state import RankingState
from gen_common.traceability.ranking.steps.cluster_and_sort_artifacts_step import ClusterAndSortArtifactsStep
from gen_common.traceability.ranking.steps.create_explanations_step import CreateExplanationsStep
from gen_common.traceability.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep


class ClusteringRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = [ClusterAndSortArtifactsStep, CreateExplanationsStep, SelectCandidateLinksStep]

    def __init__(self, args: RankingArgs, skip_summarization: bool = False):
        """
        Ranks children artifacts from most to least related to source.
        :param args: Arguments to ranking pipeline.
        :param skip_summarization: Whether to skip summarization of artifacts.
        """
        super().__init__(args, ClusteringRankingPipeline.steps, skip_summarization=skip_summarization, no_project_summary=True)
        self.args.link_threshold = CLUSTERING_LINK_THRESHOLD

    def state_class(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Gets the number of selected traces for the pipeline
        :return:  Gets the number of selected traces for the pipeline
        """
        return RankingUtil.get_input_output_counts(self.state)
