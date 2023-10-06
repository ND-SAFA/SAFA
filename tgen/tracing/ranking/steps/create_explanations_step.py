from typing import List

from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerKeys, LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.artifact_reasoning import ArtifactReasoning
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState


class CreateExplanationsStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Creates post-hoc explanations for trace-links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        a_reasonings = self._get_artifact_reasoning(args, state)
        for a_reasoning, entry in zip(a_reasonings, state.selected_entries):
            entry[TraceKeys.EXPLANATION.value] = a_reasoning.explanation

    @staticmethod
    def _get_artifact_reasoning(args: RankingArgs, state: RankingState) -> List[ArtifactReasoning]:
        """
        Creates post-hoc explanations for trace-links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        prompt_builder = CreateExplanationsStep._create_prompt_builder(state)
        filter_dataset = CreateExplanationsStep._get_dataset_with_selected_links_only(args, state)
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL:
                                                                                  PromptDataset(trace_dataset=filter_dataset)})
        save_and_load_path = LLMResponseUtil.generate_response_save_and_load_path(
            state.get_path_to_state_checkpoint(args.export_dir), "explanation_response") if args.export_dir else args.export_dir
        trainer = LLMTrainer(LLMTrainerState(llm_manager=args.explanation_llm_model, prompt_builder=prompt_builder,
                                             trainer_dataset_manager=trainer_dataset_manager))
        predictions = trainer.perform_prediction(save_and_load_path=save_and_load_path).predictions
        task_prompt: QuestionnairePrompt = prompt_builder.prompts[-1]
        tag_id = task_prompt.response_manager.get_all_tag_ids()[0]
        parsed = LLMResponseUtil.extract_predictions_from_response(predictions,
                                                                   response_prompt_ids=task_prompt.id)
        a_reasonings = [ArtifactReasoning(parsed_dict[tag_id][0], require_id=False) for parsed_dict in parsed]
        return a_reasonings

    @staticmethod
    def _get_dataset_with_selected_links_only(args: RankingArgs, state: RankingState) -> TraceDataset:
        """
        Creates a dataset containing only the selected links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        artifact_df = args.dataset.artifact_df
        selected_ids, source_layers, target_layers = [], [], []
        for entry in state.selected_entries:
            selected_ids.append(TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE], entry[TraceKeys.TARGET]))
            source, target = artifact_df.get_artifacts_from_trace(entry)
            source_layers.append(source[ArtifactKeys.LAYER_ID])
            target_layers.append(target[ArtifactKeys.LAYER_ID])
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: source_layers, LayerKeys.TARGET_TYPE: target_layers})
        trace_df = TraceDatasetCreator.generate_negative_links(layer_mapping_df=layer_df, artifact_df=artifact_df)
        trace_df = trace_df.filter_by_index(selected_ids)
        filter_dataset = TraceDataset(artifact_df=artifact_df, trace_df=trace_df,
                                      layer_df=layer_df)
        return filter_dataset

    @staticmethod
    def _create_prompt_builder(state: RankingState) -> PromptBuilder:
        """
        Creates prompt builder for ranking artifacts.
        :param state: The state of the ranking pipeline.
        :return: The prompt builder used to rank candidate children artifacts.
        """
        prompt_builder = PromptBuilder([SupportedPrompts.EXPLANATIONS_GOAL_INSTRUCTIONS.value])

        if state.project_summary is not None and len(state.project_summary) > 0:
            uses_specification = PROJECT_SUMMARY_HEADER in state.project_summary
            context_formatted = state.project_summary if uses_specification else f"# Project Summary\n{state.project_summary}"
            prompt_builder.add_prompt(Prompt(context_formatted))

        prompt_builder.add_prompt(MultiArtifactPrompt(build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                                      data_type=MultiArtifactPrompt.DataType.TRACES,
                                                      include_ids=False,
                                                      prompt_prefix=PromptUtil.as_markdown_header("ARTIFACTS")
                                                      ))
        task_prompt: QuestionnairePrompt = SupportedPrompts.RANKING_QUESTION2.value
        task_prompt.set_instructions("Use the steps below to determine if the two artifacts are traced.")
        prompt_builder.add_prompt(task_prompt)

        return prompt_builder
