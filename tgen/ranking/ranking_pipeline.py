from typing import Dict, List

from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.ranking.steps.step_complete_prompts import CompleteRankingPrompts
from tgen.ranking.steps.step_create_ranking_prompts import CreateRankingPrompts
from tgen.ranking.steps.step_process_ranking_responses import ProcessRankingResponses


class ArtifactRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    steps = [CreateRankingPrompts,
             CompleteRankingPrompts,
             ProcessRankingResponses]

    def __init__(self, artifact_map: Dict[str, str], parent_ids: List[str], parent2children: Dict[str, List[str]]):
        """
        Ranks children artifacts from most to least related to source.
        """
        args = RankingArgs(artifact_map=artifact_map, parent_ids=parent_ids,
                           parent2children=parent2children)
        super().__init__(args, ArtifactRankingPipeline.steps)

    def init_state(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState()

    def run(self) -> List[List[str]]:
        super().run()
        return self.state.processed_ranking_response
