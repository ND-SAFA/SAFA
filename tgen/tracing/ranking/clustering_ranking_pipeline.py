from typing import Dict

from tgen.common.constants.ranking_constants import CLUSTERING_LINK_THRESHOLD
from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.cluster_and_sort_artifacts_step import ClusterAndSortArtifactsStep
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep
from tgen.tracing.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep


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
