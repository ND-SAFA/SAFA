from typing import Dict, List, Union

from gen_common.data.keys.structure_keys import StructuredKeys, TraceKeys
from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.data.objects.trace import Trace
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.llm.anthropic_manager import AnthropicManager
from gen_common.llm.args.anthropic_args import AnthropicArgs
from gen_common.llm.llm_trainer import LLMTrainer
from gen_common.llm.llm_trainer_state import LLMTrainerState
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.traceability.output.abstract_trace_output import AbstractTraceOutput
from gen_common.traceability.output.trace_prediction_output import TracePredictionOutput
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.llm_ranking_pipeline import LLMRankingPipeline
from gen_common.util.ranking_util import RankingUtil

from gen.tracing.prompts.classification_prompts import CLASSIFICATION_QUESTIONNAIRE


class TracingJob(AbstractJob):
    """
    Performs filtering with little claude before ranking with big claude.
    """

    def __init__(self, job_args: JobArgs, select_top_predictions: bool = True,
                 filter_llm_manager: AbstractLLMManager = None, prediction_threshold: float = 0.5):
        """
        Constructs job for dataset at given role.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param select_top_predictions: If true, selects the top predictions. Otherwise, all predictions are returned.
        :param filter_llm_manager: The llm manager to classify trace links into buckets.
        :param prediction_threshold: The threshold (in percentile) to apply to consider a prediction as positive.
        """
        if filter_llm_manager is None:
            llm_args = AnthropicArgs(model="claude-instant-v1", temperature=0)
            filter_llm_manager = AnthropicManager(llm_args=llm_args)
        super().__init__(job_args, require_data=True)
        self.filter_llm_manager = filter_llm_manager
        self.select_top_predictions = select_top_predictions
        self.prediction_threshold = prediction_threshold

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Filters and ranks links with little claude then ranks with big claude.
        :param kwargs: Any keyword arguments.
        :return: The trace output.
        """
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets(eval=self.job_args.dataset)
        dataset: TraceDataset = self.job_args.dataset
        dataset.artifact_df.drop_large_files()
        prompt_dataset = PromptDataset(trace_dataset=dataset)

        prompt_builder = PromptBuilder(prompts=[CLASSIFICATION_QUESTIONNAIRE])
        trainer = LLMTrainer(LLMTrainerState(
            trainer_dataset_manager=trainer_dataset_manager,
            prompt_builders=prompt_builder,
            llm_manager=self.filter_llm_manager,
            **kwargs))

        prediction_output: TracePredictionOutput = trainer.perform_prediction()

        entries = prediction_output.prediction_entries
        entries = [entry for entry in entries if entry[StructuredKeys.SCORE] >= self.prediction_threshold]

        parent2entries: Dict[str, List[Trace]] = self.create_artifact_predictions_map(entries,
                                                                                      TraceKeys.parent_label().value)
        parent_ids = list(parent2entries.keys())
        parent2children: Dict[str, List[str]] = {target: [t[StructuredKeys.Trace.child_label().value] for t in entries]
                                                 for target, entries in parent2entries.items()}

        pipeline_args = RankingArgs(parent_ids=parent_ids,
                                    pre_sorted_parent2children=parent2children,
                                    dataset=prompt_dataset)
        pipeline = LLMRankingPipeline(pipeline_args)
        pipeline.run()
        parent2rankings = pipeline.state.candidate_entries
        predicted_entries = []

        for parent_id, ranked_sources in parent2rankings.items():
            target_entries = parent2entries[parent_id]
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_sources,
                                                                              original_entries=target_entries)
            predicted_entries.extend(target_predicted_entries)
        if self.select_top_predictions:
            predicted_entries = RankingUtil.select_predictions_by_thresholds(predicted_entries)
        metrics = RankingUtil.evaluate_trace_predictions(dataset.trace_df, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries, metrics=metrics)

    @staticmethod
    def create_artifact_predictions_map(predictions: List[Trace], artifact_key: str):
        """
        Groups entries by key given.
        :param predictions: The entries to group.
        :param artifact_key: The key to group by.
        :return: Map of key value to entries after they have been sorted.
        """
        id2entries: Dict[str, List[Dict]] = RankingUtil.group_trace_predictions(predictions, artifact_key)
        id2entries = {t_id: sorted(entries, key=lambda t: t[StructuredKeys.SCORE], reverse=True) for t_id, entries in
                      id2entries.items()}
        return id2entries
