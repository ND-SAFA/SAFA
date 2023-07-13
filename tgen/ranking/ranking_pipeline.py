from typing import Dict, List

from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.ranking.steps.sort_children_artifacts import PrepareChildren
from tgen.ranking.steps.step_complete_prompts import CompleteRankingPrompts
from tgen.ranking.steps.step_create_project_summary import CreateProjectSummary
from tgen.ranking.steps.step_create_ranking_prompts import CreateRankingPrompts
from tgen.ranking.steps.step_process_ranking_responses import ProcessRankingResponses
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class ArtifactRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    steps = [
        CreateProjectSummary,
        PrepareChildren,
        CreateRankingPrompts,
        CompleteRankingPrompts,
        ProcessRankingResponses]

    def __init__(self, args: RankingArgs):
        """
        Ranks children artifacts from most to least related to source.
        """
        super().__init__(args, ArtifactRankingPipeline.steps)

    def init_state(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState()

    def run(self) -> Dict[str, List[str]]:
        super().run()
        batched_ranked_children = self.state.processed_ranking_response
        parent2rankings = {source: ranked_children for source, ranked_children in zip(self.args.parent_ids, batched_ranked_children)}
        return parent2rankings
