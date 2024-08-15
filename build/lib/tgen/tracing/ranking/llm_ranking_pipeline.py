from typing import Dict, Type

from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep
from tgen.tracing.ranking.steps.process_ranking_responses_step import ProcessRankingResponsesStep
from tgen.tracing.ranking.steps.select_candidate_links_step import SelectCandidateLinksStep
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class LLMRankingPipeline(AbstractPipeline[RankingArgs, RankingState]):
    steps = [
        SortChildrenStep,
        CompleteRankingPromptsStep,
        ProcessRankingResponsesStep,
        CreateExplanationsStep,
        SelectCandidateLinksStep]

    def __init__(self, args: RankingArgs):
        """
        Ranks children artifacts from most to least related to source.
        :param args: Args to ranking pipeline.
        """
        super().__init__(args, LLMRankingPipeline.steps, no_project_summary=True)

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

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Gets the number of selected traces for the pipeline
        :return:  Gets the number of selected traces for the pipeline
        """
        selected_traces = RankingUtil.get_input_output_counts(self.state)
        n_candidate_traces = len(self.state.candidate_entries) if self.state.candidate_entries else 0
        selected_traces.update({"N Candidate Traces": n_candidate_traces})
        return selected_traces
