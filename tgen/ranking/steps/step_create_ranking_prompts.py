from typing import Dict

from tgen.pipeline.abstract_pipeline import iStep
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState


class CreateRankingPrompts(iStep[RankingArgs, RankingState]):
    def run(self, args: RankingArgs, state: RankingState) -> None:
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
            prompt = CreateRankingPrompts.create_prompts(artifact_map, p_name, args, state)
            prompts.append(prompt)

        state.ranking_prompts = prompts

    @staticmethod
    def create_prompts(artifact_map: Dict[str, str],
                       parent_id: str,
                       args: RankingArgs,
                       state: RankingState) -> str:
        """
        Creates ranking prompt for parent artifact.
        :param artifact_map: Map of artifact id to body.
        :param parent_id: The id of the parent to create prompt for.
        :param args: The ranking pipeline configuration.
        :param state: The state of the current ranking run.
        :return: The ranking prompt.
        """
        target_names = args.parent2children[parent_id]
        source_body = artifact_map[parent_id]
        prompt_builder = RankingPromptBuilder(goal=state.ranking_goal,
                                              instructions=state.ranking_instructions,
                                              query=source_body,
                                              body_title="# Artifacts")
        for target_index, target_artifact_name in enumerate(target_names):
            prompt_builder.with_artifact(target_index, artifact_map[target_artifact_name])
        if parent_id in state.source2reason:
            prompt_builder.with_context(state.source2reason[parent_id])
        prompt = prompt_builder.get()
        return prompt
