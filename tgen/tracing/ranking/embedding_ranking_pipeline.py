from typing import Dict

from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter
from tgen.tracing.ranking.steps.calculate_composite_scores_step import CalculateCompositeScoreStep
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep
from tgen.tracing.ranking.steps.filter_scores_step import FilterScoresStep
from tgen.tracing.ranking.steps.re_rank_step import ReRankStep
from tgen.tracing.ranking.steps.rewrite_artifacts_step import RewriteArtifactsStep
from tgen.tracing.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class EmbeddingRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = [RewriteArtifactsStep, SortChildrenStep, FilterScoresStep, CalculateCompositeScoreStep, SelectCandidateLinksStep,
             ReRankStep, CreateExplanationsStep]

    def __init__(self, args: RankingArgs, skip_summarization: bool = False):
        """
        Ranks children artifacts from most to least related to source.
        :param args: Arguments to ranking pipeline.
        :param skip_summarization: Whether to skip summarization of artifacts.
        """
        super().__init__(args, EmbeddingRankingPipeline.steps, skip_summarization=skip_summarization, no_project_summary=True)

    def state_class(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState

    def run(self, **kwargs) -> None:
        """

        :return: List of parents mapped to their ranked children.
        """
        self.args.sorter = SupportedSorter.TRANSFORMER.name
        super().run()

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Gets the number of selected traces for the pipeline
        :return:  Gets the number of selected traces for the pipeline
        """
        return RankingUtil.get_input_output_counts(self.state)
