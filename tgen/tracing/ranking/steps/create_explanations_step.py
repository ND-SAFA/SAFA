from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER
from tgen.common.util.dict_util import DictUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState


class CreateExplanationsStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Creates post-hoc explanations for trace-links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        prompt_builder = CreateExplanationsStep.create_prompt_builder(state)
        prompts = []
        for entry in state.selected_entries:
            child = args.dataset.artifact_df.get_artifact(entry[TraceKeys.SOURCE])
            parent = args.dataset.artifact_df.get_artifact(entry[TraceKeys.TARGET])
            artifacts = [{ArtifactKeys.ID: "parent",
                          ArtifactKeys.CONTENT: parent[ArtifactKeys.CONTENT]},
                         {ArtifactKeys.ID: "child",
                          ArtifactKeys.CONTENT: child[ArtifactKeys.CONTENT]}]
            prompt = prompt_builder.build(artifacts=artifacts)[PromptKeys.PROMPT]
            prompts.append(prompt)
        kwargs = {PromptKeys.PROMPT.value: prompts}
        if args.ranking_llm_model:
            DictUtil.update_kwarg_values(kwargs, model=args.explanation_llm_model)
        batch_response = args.llm_manager.make_completion_request(LLMCompletionType.GENERATION, **kwargs)

        return batch_response

    @staticmethod
    def create_prompt_builder(state: RankingState) -> PromptBuilder:
        """
        Creates prompt builder for ranking artifacts.
        :param state: The state of the ranking pipeline.
        :return: The prompt builder used to rank candidate children artifacts.
        """
        prompt_builder = PromptBuilder()

        if state.project_summary is not None and len(state.project_summary) > 0:
            uses_specification = PROJECT_SUMMARY_HEADER in state.project_summary
            context_formatted = state.project_summary if uses_specification else f"# Project Summary\n{state.project_summary}"
            prompt_builder.add_prompt(Prompt(context_formatted))

        prompt_builder.add_prompt(MultiArtifactPrompt(build_method=MultiArtifactPrompt.BuildMethod.XML,
                                                      include_ids=True))

        for q in (SupportedPrompts.RANKING_QUESTION1.value, SupportedPrompts.RANKING_QUESTION2.value):
            prompt_builder.add_prompt(q)

        return prompt_builder
