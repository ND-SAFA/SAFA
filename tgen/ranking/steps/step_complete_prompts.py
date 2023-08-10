import os.path

from tgen.common.util.file_util import FileUtil
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
        TRACE_FILE_NAME = "tracing_response.yaml"
        TRACE_FILE_PATH = args.get_path(TRACE_FILE_NAME)

        if TRACE_FILE_PATH is not None and os.path.exists(TRACE_FILE_PATH):
            text = FileUtil.read_yaml(TRACE_FILE_PATH)
            generation_response = GenerationResponse(**text)
        else:
            generation_response = self.complete_ranking_prompts(args, state)
            args.save(generation_response, "tracing_response.yaml")
        state.ranking_responses = generation_response

    @staticmethod
    def complete_ranking_prompts(args: RankingArgs, state: RankingState) -> GenerationResponse:
        """
        Completes the ranking prompts.
        :param args: The pipeline configuration.
        :param state: The ranking store.
        :return: None
        """
        kwargs = {}
        if args.ranking_llm_model:
            kwargs["model"] = args.ranking_llm_model
        batch_response = complete_prompts(state.ranking_prompts,
                                          temperature=0,
                                          max_tokens=args.n_completion_tokens,
                                          **kwargs)
        return batch_response
