from typing import Dict, List, Union

from common_resources.data.keys.structure_keys import StructuredKeys, TraceKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.llm.anthropic_manager import AnthropicManager
from common_resources.llm.args.anthropic_args import AnthropicArgs

from tgen.common.objects.trace import Trace
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.llm_ranking_pipeline import LLMRankingPipeline


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

        prompt_builder = PromptBuilder(prompts=[SupportedPrompts.TGEN_CLASSIFICATION.value])
        base_tracing_job = LLMJob(trainer_dataset_manager,
                                  task=TrainerTask.PREDICT,
                                  llm_manager=self.filter_llm_manager,
                                  prompt_builder=prompt_builder)
        prediction_output: TracePredictionOutput = base_tracing_job.run().body

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
