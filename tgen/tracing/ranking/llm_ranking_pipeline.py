import os
from typing import Type

from tgen.state.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep
from tgen.tracing.ranking.steps.create_project_summary_step import CreateProjectSummaryStep
from tgen.tracing.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep
from tgen.tracing.ranking.steps.process_ranking_responses_step import ProcessRankingResponsesStep
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class LLMRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    steps = [
        CreateProjectSummaryStep,
        SortChildrenStep,
        CompleteRankingPromptsStep,
        ProcessRankingResponsesStep,
        SelectCandidateLinksStep]

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

    def run(self) -> None:
        """
        Runs the pipeline to rank the artifacts
        :return: a dictionary mapping the parent to its child rankings
        and a dictionary mapping parent to the explanations for its links
        """
        super().run()
