from typing import Dict

from tgen.common.util.str_util import StrUtil
from tgen.constants.tgen_constants import BODY_ARTIFACT_TITLE, SUMMARY_TITLE
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateRankingPrompts(AbstractPipelineStep[RankingArgs, RankingState]):
    def _run(self, args: RankingArgs, state: RankingState) -> None:
        self.create_ranking_prompts(args, state)

    @staticmethod
    def create_ranking_prompts(args: RankingArgs, state: RankingState) -> None:
        """
        Creates the prompts to rank children.
        :param args: The configuration of the ranking pipeline.
        :param state: The state of the ranking run.
        :return: None
        """
        artifact_map = args.artifact_map
        parent_names = args.parent_ids

        prompts = []
        for p_name in parent_names:
            prompt = CreateRankingPrompts.create_prompts(artifact_map, p_name, args, state, args.max_children_per_query)
            prompts.append(prompt)

        state.ranking_prompts = prompts

    @staticmethod
    def create_prompts(artifact_map: Dict[str, str],
                       parent_id: str,
                       args: RankingArgs,
                       state: RankingState, max_children: int = None) -> str:
        """
        Creates ranking prompt for parent artifact.
        :param artifact_map: Map of artifact id to body.
        :param parent_id: The id of the parent to create prompt for.
        :param args: The configuration of the ranking pipeline.
        :param state: The state of the current ranking run.
        :return: The ranking prompt.
        """
        target_names = state.sorted_parent2children[parent_id][:max_children]
        source_body = artifact_map[parent_id]
        prompt_builder = RankingPromptBuilder(goal=args.ranking_goal,
                                              instructions=args.ranking_instructions,
                                              query=source_body,
                                              query_tag=args.query_tag,
                                              body_title=BODY_ARTIFACT_TITLE)
        if state.project_summary is not None and len(state.project_summary) > 0:
            uses_specification = SUMMARY_TITLE in state.project_summary
            context_formatted = state.project_summary if uses_specification else f"# Project Summary\n{state.project_summary}"
            prompt_builder.with_context(context_formatted)

        use_name = not StrUtil.is_uuid(target_names[0])
        for target_index, target_artifact_name in enumerate(target_names):
            kwargs = {}
            if use_name:
                kwargs["name"] = target_artifact_name
            prompt_builder.with_artifact(target_index, artifact_map[target_artifact_name], **kwargs)
        prompt = prompt_builder.get()
        return prompt
