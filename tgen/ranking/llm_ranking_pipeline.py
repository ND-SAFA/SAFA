import os
from typing import Dict, List

from tgen.common.util.ranking_util import RankingUtil
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.ranking.steps.sort_children_artifacts import PrepareChildren
from tgen.ranking.steps.step_complete_prompts import CompleteRankingPrompts
from tgen.ranking.steps.step_create_project_summary import CreateProjectSummary
from tgen.ranking.steps.step_create_ranking_prompts import CreateRankingPrompts
from tgen.ranking.steps.step_process_ranking_responses import ProcessRankingResponses
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class LLMRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
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
        super().__init__(args, LLMRankingPipeline.steps)

    def init_state(self) -> RankingState:
        """
        Creates new ranking state.
        :return: The new state.
        """
        return RankingState()

    def run(self) -> List[Dict]:
        if self.args.export_dir is not None:
            os.makedirs(self.args.export_dir, exist_ok=True)
        super().run()
        batched_ranked_children = self.state.ranked_children
        parent2rankings = {source: ranked_children for source, ranked_children in zip(self.args.parent_ids, batched_ranked_children)}
        parent2explanations = {s: e for s, e in zip(self.args.parent_ids, self.state.ranked_children_explanations)}
        prediction_entries = RankingUtil.ranking_to_predictions(parent2rankings, parent2explanations=parent2explanations)
        return prediction_entries
