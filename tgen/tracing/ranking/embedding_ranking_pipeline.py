from typing import Dict

from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep
from tgen.tracing.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class EmbeddingRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = [SortChildrenStep, CreateExplanationsStep, SelectCandidateLinksStep]

    def __init__(self, args: RankingArgs, embedding_manager: EmbeddingsManager = None):
        """
        Ranks children artifacts from most to least related to source.
        :param args: Arguments to ranking pipeline.
        :param embedding_manager: Stores and computes artifact embeddings.
        """
        super().__init__(args, EmbeddingRankingPipeline.steps)
        self.state.embedding_manager = embedding_manager

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

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Gets the number of selected traces for the pipeline
        :return:  Gets the number of selected traces for the pipeline
        """
        return RankingUtil.get_input_output_counts(self.state)
