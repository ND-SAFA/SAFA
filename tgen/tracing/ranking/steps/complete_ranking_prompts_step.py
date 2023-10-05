from typing import List, Dict

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER, ARTIFACT_HEADER, RANKING_PARENT_TAG
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState


class CompleteRankingPromptsStep(AbstractPipelineStep[RankingArgs, RankingState]):

    @overrides(AbstractPipelineStep)
    def run(self, args: RankingArgs, state: RankingState, re_run: bool = False) -> bool:
        """
        Ensures the prompt builder is saved to state
        :param args: The pipeline arguments / configuration.
        :param state: The state of the current run.
        :param re_run: Whether to rerun the step or not
        :return: Whether the step ran or not
        """
        state.prompt_builder = CompleteRankingPromptsStep.create_ranking_prompt_builder(state)
        return super().run(args, state, re_run)

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
        prompts = CompleteRankingPromptsStep.create_ranking_prompts(args, state)
        kwargs = {PromptKeys.PROMPT.value: prompts}
        if args.ranking_llm_model:
            DictUtil.update_kwarg_values(kwargs, model=args.ranking_llm_model)
        batch_response = args.llm_manager.make_completion_request(LLMCompletionType.GENERATION, **kwargs)

        return batch_response

    @staticmethod
    def create_ranking_prompts(args: RankingArgs, state: RankingState) -> List[Prompt]:
        """
        Creates the prompts to rank children.
        :param args: The configuration of the ranking pipeline.
        :param state: The state of the ranking run.
        :return: The list of prompts created
        """
        parent_names = args.parent_ids

        prompts = []
        for p_name in parent_names:
            artifact_map = args.dataset.artifact_df.to_map()
            prompt = CompleteRankingPromptsStep.create_prompts(p_name, artifact_map, state.prompt_builder, args, state)
            prompts.append(prompt)
        return prompts

    @staticmethod
    def create_prompts(parent_id: str, artifact_map: Dict, prompt_builder: PromptBuilder, args: RankingArgs, state: RankingState) -> Prompt:
        """
        Creates ranking prompt for parent artifact.
        :param parent_id: The id of the parent to create prompt for.
        :param prompt_builder: The prompt builder to use to create the prompt
        :param artifact_map: Maps artifact id to content
        :param args: The arguments to the ranking pipeline
        :param state: The state of the current ranking run.
        :return: The ranking prompt.
        """
        max_children = args.max_children_per_query
        entries = state.sorted_parent2children[parent_id][:max_children]
        source_body = artifact_map[parent_id]
        artifacts = [EnumDict({ArtifactKeys.ID: i, ArtifactKeys.CONTENT: artifact_map[entry[TraceKeys.SOURCE]]})
                     for i, entry in enumerate(entries)]

        prompt_dict = prompt_builder.build(model_format_args=AnthropicManager.prompt_args,
                                           parent_body=source_body,
                                           artifacts=artifacts)
        prompt = prompt_dict[PromptKeys.PROMPT]

        return prompt

    @staticmethod
    def create_ranking_prompt_builder(state: RankingState) -> PromptBuilder:
        """
        Creates prompt builder for ranking artifacts.
        :param state: The state of the ranking pipeline.
        :return: The prompt builder used to rank candidate children artifacts.
        """
        prompt_builder = PromptBuilder(prompts=[
            SupportedPrompts.RANKING_GOAL_INSTRUCTIONS.value,
            Prompt(PromptUtil.create_xml(RANKING_PARENT_TAG, '{parent_body}', prefix=NEW_LINE, suffix=NEW_LINE)),
        ])

        if state.project_summary is not None and len(state.project_summary) > 0:
            uses_specification = PROJECT_SUMMARY_HEADER in state.project_summary
            context_formatted = state.project_summary if uses_specification else f"# Project Summary\n{state.project_summary}"
            prompt_builder.add_prompt(Prompt(context_formatted))

        prompt_builder.add_prompt(MultiArtifactPrompt(prompt_prefix=PromptUtil.as_markdown_header(ARTIFACT_HEADER),
                                                      build_method=MultiArtifactPrompt.BuildMethod.XML,
                                                      include_ids=True))

        for q in (SupportedPrompts.RANKING_QUESTION1.value, SupportedPrompts.RANKING_QUESTION2.value):
            prompt_builder.add_prompt(q)

        return prompt_builder
