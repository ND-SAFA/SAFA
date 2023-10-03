from tgen.data.keys.prompt_keys import PromptKeys
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


class CompleteRankingPrompts(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Completes the ranking prompts.
        :param args: The pipeline arguments / configuration.
        :param state: The state of the current run.
        :return: None
        """
        generation_response = self.complete_ranking_prompts(args, state)
        state.ranking_responses = generation_response

    @staticmethod
    def complete_ranking_prompts(args: RankingArgs, state: RankingState) -> GenerationResponse:
        """
        Completes the ranking prompts.
        :param args: The pipeline configuration.
        :param state: The ranking store.
        :return: None
        """
        kwargs = {PromptKeys.PROMPT.value: state.ranking_prompts}
        if args.ranking_llm_model:
            kwargs["model"] = args.ranking_llm_model
        batch_response = args.llm_manager.make_completion_request(LLMCompletionType.GENERATION, **kwargs)

        return batch_response
