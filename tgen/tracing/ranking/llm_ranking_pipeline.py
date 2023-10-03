import os
from typing import Dict, Tuple, Type, List

from tgen.common.util.enum_util import EnumDict
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState
from tgen.tracing.ranking.steps.sort_children_step import SortChildren
from tgen.tracing.ranking.steps.step_complete_prompts import CompleteRankingPrompts
from tgen.tracing.ranking.steps.step_create_project_summary import CreateProjectSummary
from tgen.tracing.ranking.steps.step_create_ranking_prompts import CreateRankingPrompts
from tgen.tracing.ranking.steps.step_process_ranking_responses import ProcessRankingResponses


class LLMRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    steps = [
        CreateProjectSummary,
        SortChildren,
        CreateRankingPrompts,
        CompleteRankingPrompts,
        ProcessRankingResponses]

    def __init__(self, args: RankingArgs):
        """
        Ranks children artifacts from most to least related to source.
        """
        super().__init__(args, LLMRankingPipeline.steps)

    def state_class(self) -> Type:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """
        return RankingState

    def run(self) -> List[TracePredictionEntry]:
        """
        Runs the pipeline to rank the artifacts
        :return: a dictionary mapping the parent to its child rankings
        and a dictionary mapping parent to the explanations for its links
        """
        if self.args.export_dir:
            os.makedirs(self.args.export_dir, exist_ok=True)
            self.state.export_dir = self.args.export_dir
        super().run()
        prediction_entries = self.state.children_entries
        return prediction_entries
