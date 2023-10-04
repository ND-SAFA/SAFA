import os

from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter
from tgen.tracing.ranking.steps.filter_links_below_threshold_step import FilterLinksBelowThresholdStep
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class EmbeddingRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = [SortChildrenStep, FilterLinksBelowThresholdStep]

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
        if self.args.export_dir:
            os.makedirs(self.args.export_dir, exist_ok=True)
        self.args.sorter = SupportedSorter.EMBEDDING.name
        super().run()
