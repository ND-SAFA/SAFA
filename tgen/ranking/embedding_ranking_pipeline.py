import os
from typing import Dict, List

from tgen.common.util.ranking_util import RankingUtil
from tgen.ranking.common.vsm_sorter import embedding_sorter
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class EmbeddingRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    """
    Ranks a set of artifacts by using their embeddings to their parents.
    """
    steps = []

    def __init__(self, args: RankingArgs):
        """
        Ranks children artifacts from most to least related to source.
        """
        super().__init__(args, EmbeddingRankingPipeline.steps)

    def init_state(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState()

    def run(self) -> Dict[str, List[str]]:
        """

        :return: List of parents mapped to their ranked children.
        """
        if self.args.export_dir is not None:
            os.makedirs(self.args.export_dir, exist_ok=True)
        super().run()
        parent2rankings = embedding_sorter(self.args.parent_ids, self.args.children_ids, self.args.artifact_map, return_scores=False)
        prediction_entries = RankingUtil.ranking_to_predictions(parent2rankings)
        return prediction_entries
