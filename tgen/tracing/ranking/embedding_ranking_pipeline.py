import os

from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep
from tgen.tracing.ranking.steps.create_project_summary_step import CreateProjectSummaryStep
from tgen.tracing.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class EmbeddingRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = [CreateProjectSummaryStep, SortChildrenStep, CreateExplanationsStep, SelectCandidateLinksStep]

    def __init__(self, args: RankingArgs):
        """
        Ranks children artifacts from most to least related to source.
        """
        super().__init__(args, EmbeddingRankingPipeline.steps)

    def state_class(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState

    def run(self) -> None:
        """

        :return: List of parents mapped to their ranked children.
        """
        self.args.sorter = SupportedSorter.EMBEDDING.name
        super().run()
