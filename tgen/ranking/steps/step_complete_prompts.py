import os

from tgen.models.llm.llm_responses import GenerationResponse
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger


class CompleteRankingPrompts(AbstractPipelineStep[RankingArgs, RankingState]):

    def run(self, args: RankingArgs, state: RankingState) -> None:
        export_path = os.path.join(args.export_dir, "responses.yaml")
        if os.path.exists(export_path) and args.load_response:
            logger.info(f"Loading generation responses from: {export_path}")
            yaml_content = FileUtil.read_yaml(export_path)
            state.ranking_responses = GenerationResponse(**yaml_content)
        else:
            generation_response = self.complete_ranking_prompts(args, state)
            state.ranking_responses = generation_response
            FileUtil.write_yaml(generation_response, export_path)
            logger.info(f"Wrote generation responses to: {export_path}")

    @staticmethod
    def complete_ranking_prompts(args: RankingArgs, state: RankingState) -> None:
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
