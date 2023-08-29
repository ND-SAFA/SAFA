from typing import Dict

from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


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
        artifacts = [EnumDict({ArtifactKeys.ID: i, ArtifactKeys.CONTENT: artifact_map[a_id]}) for i, a_id in enumerate(target_names)]

        prompt_builder = CreateRankingPrompts.create_ranking_prompt_builder(args, state, source_body)
        prompt_dict = prompt_builder.build(model_format_args=AnthropicManager.prompt_args,
                                           artifacts=artifacts)
        prompt = prompt_dict[PromptKeys.PROMPT]
        state.prompt_builders.append(prompt_builder)

        return prompt

    @staticmethod
    def create_ranking_prompt_builder(args: RankingArgs, state: RankingState, parent_body: str) -> PromptBuilder:
        """
        Creates prompt builder for ranking artifacts.
        :param args: The arguments to the ranking pipeline.
        :param state: The state of the ranking pipeline.
        :param parent_body: The body of the parent artifact.
        :param include_ids: Whether to include artifact ids.
        :return: The prompt builder used to rank candidate children artifacts.
        """
        prompt_builder = PromptBuilder(prompts=[
            Prompt(args.ranking_goal),
            Prompt(PromptUtil.create_xml(args.query_tag, parent_body, prefix="\n", suffix="\n")),
        ])

        if state.project_summary is not None and len(state.project_summary) > 0:
            uses_specification = PROJECT_SUMMARY_HEADER in state.project_summary
            context_formatted = state.project_summary if uses_specification else f"# Project Summary\n{state.project_summary}"
            prompt_builder.add_prompt(Prompt(context_formatted))

        prompt_builder.add_prompt(MultiArtifactPrompt(prompt_prefix=PromptUtil.as_markdown_header(args.artifact_header),
                                                      build_method=MultiArtifactPrompt.BuildMethod.XML,
                                                      include_ids=True))

        question_prompts = [QuestionPrompt(question=q, response_manager=rm) for q, rm in
                            args.ranking_questions]
        prompt_builder.add_prompt(QuestionnairePrompt(question_prompts=question_prompts, instructions=args.ranking_instructions))

        return prompt_builder
