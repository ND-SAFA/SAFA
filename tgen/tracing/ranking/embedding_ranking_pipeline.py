import os

from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState
from tgen.tracing.ranking.steps.sort_children_step import SortChildren


class EmbeddingRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = [SortChildren]

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
        super().run()
        self.state.children_entries = [entry for entries in self.state.sorted_parent2children.values() for entry in entries]
