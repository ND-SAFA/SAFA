from tgen.models.llm.llm_responses import GenerationResponse
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CompleteRankingPrompts(AbstractPipelineStep[RankingArgs, RankingState]):

    def run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Completes the ranking prompts.
        :param args: The pipeline arguments / configuration.
        :param state: The state of the current run.
        :return: None
        """
        generation_response = self.complete_ranking_prompts(args, state)
        state.ranking_responses = generation_response
        args.save(generation_response, "tracing_response.yaml")

    @staticmethod
    def complete_ranking_prompts(args: RankingArgs, state: RankingState) -> GenerationResponse:
        """
        Completes the ranking prompts.
        :param args: The pipeline configuration.
        :param state: The ranking store.
        :return: None
        """
        kwargs = {}
        if args.model:
            kwargs["model"] = args.model
        batch_response = complete_prompts(state.ranking_prompts, max_tokens=args.n_completion_tokens, **kwargs)
        return batch_response
