import os
from typing import Dict, List

from tgen.data.dataframes.trace_dataframe import TraceKeys
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
        parent2rankings = embedding_sorter(self.args.parent_ids, self.args.children_ids, self.args.artifact_map,
                                           return_scores=True, model_name=self.args.embedding_model)
        prediction_entries = []
        for parent, parent_payload in parent2rankings.items():
            for child, score in zip(*parent_payload):
                entry = {
                    TraceKeys.TARGET.value: parent,
                    TraceKeys.SOURCE.value: child,
                    TraceKeys.SCORE.value: score
                }
                prediction_entries.append(entry)
        return prediction_entries
