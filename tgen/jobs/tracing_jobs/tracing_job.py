from typing import Dict, List, Union

from tgen.common.util.data_structure_util import DataStructureUtil
from tgen.common.util.ranking_util import RankingUtil
from tgen.core.args.anthropic_args import AnthropicArgs
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.ranking.llm_ranking_pipeline import LLMRankingPipeline
from tgen.ranking.ranking_args import RankingArgs


class TracingJob(AbstractJob):
    """
    Performs filtering with little claude before ranking with big claude.
    """

    def __init__(self, dataset_creator: AbstractDatasetCreator, select_top_predictions: bool = True,
                 filter_llm_manager: AbstractLLMManager = None, prediction_threshold: float = 0.5):
        """
        Constructs job for dataset at given role.
        :param dataset_creator: Creates the dataset to evaluate.
        :param select_top_predictions: If true, selects the top predictions. Otherwise, all predictions are returned.
        :param filter_llm_manager: The llm manager to classify trace links into buckets.
        :param prediction_threshold: The threshold (in percentile) to apply to consider a prediction as positive.
        """
        if filter_llm_manager is None:
            llm_args = AnthropicArgs(model="claude-instant-v1", temperature=0)
            filter_llm_manager = AnthropicManager(llm_args=llm_args)
        super().__init__()
        self.dataset_creator = dataset_creator
        self.filter_llm_manager = filter_llm_manager
        self.select_top_predictions = select_top_predictions
        self.prediction_threshold = prediction_threshold

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Filters and ranks links with little claude then ranks with big claude.
        :param kwargs: Any keyword arguments.
        :return: The trace output.
        """
        trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=self.dataset_creator)
        dataset: TraceDataset = trainer_dataset_manager[DatasetRole.EVAL]
        artifact_map = DataStructureUtil.create_artifact_map(dataset.artifact_df)

        prompt_builder = PromptBuilder(prompts=[SupportedPrompts.TGEN_CLASSIFICATION.value])
        base_tracing_job = LLMJob(trainer_dataset_manager,
                                  task=TrainerTask.PREDICT,
                                  llm_manager=self.filter_llm_manager,
                                  prompt_builder=prompt_builder)
        prediction_output: TracePredictionOutput = base_tracing_job.run().body

        entries = prediction_output.prediction_entries
        entries = [entry for entry in entries if entry[StructuredKeys.SCORE] >= self.prediction_threshold]

        parent2entries: Dict[str, List[TracePredictionEntry]] = self.create_artifact_predictions_map(entries, TraceKeys.TARGET.value)
        parent_ids = list(parent2entries.keys())
        parent2children: Dict[str, List[str]] = {target: [t[StructuredKeys.SCORE] for t in entries] for target, entries in
                                                 parent2entries.items()}

        pipeline_args = RankingArgs(parent_ids=parent_ids,
                                    parent2children=parent2children,
                                    artifact_map=artifact_map)
        pipeline = LLMRankingPipeline(pipeline_args)
        parent2rankings = pipeline.run()
        predicted_entries = []

        for parent_id, ranked_sources in parent2rankings.items():
            target_entries = parent2entries[parent_id]
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_sources,
                                                                              original_entries=target_entries)
            predicted_entries.extend(target_predicted_entries)
        if self.select_top_predictions:
            predicted_entries = RankingUtil.select_predictions(predicted_entries)
        RankingUtil.calculate_ranking_metrics(dataset, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    @staticmethod
    def create_artifact_predictions_map(predictions: List[TracePredictionEntry], artifact_key: str):
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
