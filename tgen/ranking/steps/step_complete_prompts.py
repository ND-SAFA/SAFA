from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState


class CompleteRankingPrompts(AbstractPipelineStep[RankingArgs, RankingState]):
    def run(self, args: RankingArgs, state: RankingState) -> None:
        self.complete_ranking_prompts(args, state)

    @staticmethod
    def complete_ranking_prompts(args: RankingArgs, state: RankingState) -> None:
        """
        Completes the ranking prompts.
        :param state: The ranking store.
        :return: None
        """
        batch_response = complete_prompts(state.ranking_prompts, max_tokens=2000)
        state.ranking_responses = batch_response
