from typing import Dict, List

from tgen.common.constants.ranking_constants import FIRST_PASS_THRESHOLD_DELTA, RANKING_MAX_SCORE, RANKING_MIN_SCORE, \
    RANKING_SCORE_TAG
from common_resources.tools.util.llm_response_util import LLMResponseUtil
from common_resources.tools.util.math_util import MathUtil
from common_resources.tools.util.prompt_util import PromptUtil
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.tracing.ranking.common.artifact_reasoning import ArtifactReasoning
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class CreateExplanationsStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Creates post-hoc explanations for trace-links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        if not args.generate_explanations:
            return
        parsed_predictions = self._generate_predictions(args, state)
        artifact_reasonings = CreateExplanationsStep._create_artifact_reasonings(parsed_predictions)
        for artifact_reasoning, entry in zip(artifact_reasonings, state.get_current_entries()):
            entry[TraceKeys.EXPLANATION] = artifact_reasoning.explanation
            entry[TraceKeys.SCORE] = MathUtil.calculate_weighted_score(scoreA=artifact_reasoning.score,
                                                                       scoreB=entry[TraceKeys.SCORE],
                                                                       weight_of_scoreA=args.weight_of_explanation_scores)

    @staticmethod
    def _generate_predictions(args: RankingArgs, state: RankingState) -> List[Dict]:
        """
        Creates post-hoc explanations for trace-links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """

        filter_dataset = CreateExplanationsStep._get_dataset_with_selected_links_only(args, state)
        prompt_builder = CreateExplanationsStep._create_prompt_builder(state)
        prompt_builder.format_prompts_with_var(target_type=args.types_to_trace[0], source_type=args.types_to_trace[1])

        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets(eval=PromptDataset(trace_dataset=filter_dataset))
        save_and_load_path = LLMResponseUtil.generate_response_save_and_load_path(
            state.get_path_to_state_checkpoint(args.export_dir), "explanation_response") if args.export_dir else args.export_dir
        trainer = LLMTrainer(LLMTrainerState(llm_manager=args.explanation_llm_model, prompt_builders=prompt_builder,
                                             trainer_dataset_manager=trainer_dataset_manager))
        predictions = trainer.perform_prediction(save_and_load_path=save_and_load_path).predictions
        task_prompt: QuestionnairePrompt = prompt_builder.prompts[-1]
        parsed = LLMResponseUtil.extract_predictions_from_response(predictions,
                                                                   response_prompt_ids=task_prompt.args.prompt_id)

        return parsed

    @staticmethod
    def _create_artifact_reasonings(parsed_predictions: List[Dict]) -> List[ArtifactReasoning]:
        """
        Creates artifact reasoning from the predicted explanations
        :param parsed_predictions: The parsed predictions
        :return: A list of artifact reasoning created from the predictions
        """
        artifact_reasonings = []
        for parsed_dict in parsed_predictions:
            artifact_reasoning = ArtifactReasoning(parsed_dict, require_id=False)
            artifact_reasonings.append(artifact_reasoning)
        return artifact_reasonings

    @staticmethod
    def _get_dataset_with_selected_links_only(args: RankingArgs, state: RankingState) -> TraceDataset:
        """
        Creates a dataset containing only the selected links
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        artifact_df = args.dataset.artifact_df
        selected_ids, layers = [], set()
        if args.selection_method:
            state.selected_entries = args.selection_method.value.select(state.get_current_entries(),
                                                                        threshold=args.link_threshold - FIRST_PASS_THRESHOLD_DELTA,
                                                                        parent_thresholds=tuple([t - FIRST_PASS_THRESHOLD_DELTA
                                                                                                 for t in args.parent_thresholds]))

        for entry in state.get_current_entries():
            selected_ids.append(TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE], entry[TraceKeys.TARGET]))
            source, target = artifact_df.get_artifacts_from_trace(entry)
            layers.add((source[ArtifactKeys.LAYER_ID], target[ArtifactKeys.LAYER_ID]))
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [source for source, _ in layers],
                                   LayerKeys.TARGET_TYPE: [target for _, target in layers]})
        trace_df = TraceDatasetCreator.generate_negative_links(layer_df=layer_df, artifact_df=artifact_df)
        trace_df = trace_df.filter_by_index(selected_ids)
        expected_order = [TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE], entry[TraceKeys.TARGET])
                          for entry in state.get_current_entries()]
        trace_df = TraceDataFrame(trace_df.reindex(expected_order))
        filter_dataset = TraceDataset(artifact_df=artifact_df, trace_df=trace_df,
                                      layer_df=layer_df, randomize=False)
        return filter_dataset

    @staticmethod
    def _create_prompt_builder(state: RankingState) -> PromptBuilder:
        """
        Creates prompt builder for ranking artifacts.
        :param dataset: The dataset containing the trace links to be used in the prompts
        :param state: The state of the ranking pipeline.
        :return: The prompt builder used to rank candidate children artifacts.
        """
        scores = RankingUtil.get_scores(state.get_current_entries())
        converted_scores = [CreateExplanationsStep._convert_normalized_score_to_ranking_range(score) for score in scores]
        prompt_builder = PromptBuilder([SupportedPrompts.EXPLANATIONS_GOAL_INSTRUCTIONS.value], orig_score=converted_scores)

        RankingUtil.add_project_summary_prompt(prompt_builder, state)
        prompt_builder.add_prompt(MultiArtifactPrompt(build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                                      data_type=MultiArtifactPrompt.DataType.TRACES,
                                                      include_ids=True,
                                                      prompt_start=PromptUtil.as_markdown_header("ARTIFACTS")
                                                      ))
        task_prompt: QuestionnairePrompt = SupportedPrompts.EXPLANATION_TASK.value
        score_prompt = task_prompt.get_prompt_by_primary_tag(RANKING_SCORE_TAG)
        score_prompt.value += "Remember the original score for the relationship was {orig_score}. " \
                              "Use this to guide your decision but you may adjust it if you do not believe it accurately reflects " \
                              "the strength of the relationship."
        prompt_builder.add_prompt(task_prompt)

        return prompt_builder

    @staticmethod
    def _convert_normalized_score_to_ranking_range(score: float) -> float:
        """
        Converts a score between 0-1 to the range used in ranking
        :param score: The score to convert
        :return: The converted score
        """
        return MathUtil.convert_to_new_range(score, (0, 1), (RANKING_MIN_SCORE, RANKING_MAX_SCORE))
