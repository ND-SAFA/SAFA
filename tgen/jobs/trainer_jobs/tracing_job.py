from typing import Dict, List, Union

import pandas as pd

from paper.pipeline.base import RankingStore
from paper.pipeline.map_step import create_increment_list
from paper.pipeline.ranking_step import RankingStep
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.train.trainers.trainer_task import TrainerTask


class TracingJob(LLMJob):
    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, dataset_role: DatasetRole = DatasetRole.EVAL):
        super().__init__(trainer_dataset_manager, task=TrainerTask.PREDICT)
        self.dataset_role = dataset_role

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        THRESHOLD = 0.5
        dataset: TraceDataset = self.trainer_dataset_manager[self.dataset_role]
        artifact_map = self.create_artifact_map(dataset.artifact_df)

        prediction_output: TracePredictionOutput = super()._run(**kwargs)
        entries = prediction_output.prediction_entries
        entries = [entry for entry in entries if entry["score"] >= THRESHOLD]

        indices_defined = [TraceDataFrame.generate_link_id(entry["source"], entry["target"]) for entry in entries]
        trace_df = dataset.trace_df.filter_by_index(indices_defined)

        target2entries: Dict[str, List[TracePredictionEntry]] = self.create_id_to_entries(entries, "target")
        targets = list(target2entries.keys())
        target2sources: Dict[str, List[str]] = {target: [t["source"] for t in entries] for target, entries in target2entries.items()}

        ranking_store = RankingStore()
        ranking_store.artifact_map = artifact_map
        ranking_store.source_ids = targets  # flip flop because in study source = target
        ranking_store.source2targets = target2sources
        ranking_step = RankingStep()
        ranking_step(ranking_store)
        batch_ranked_targets = ranking_store.processed_ranking_response

        predicted_entries = []

        for i, ranked_sources in enumerate(batch_ranked_targets):
            target = targets[i]
            target_entries = target2entries[target]
            target_predicted_entries = self.parse_ranking_response(target, target_entries, ranked_sources)
            predicted_entries.extend(target_predicted_entries)

        link_ids = [TraceDataFrame.generate_link_id(entry["source"], entry["target"]) for entry in predicted_entries]
        scores = [entry["score"] for entry in predicted_entries]
        metrics_manager = MetricsManager(trace_df, predicted_similarities=scores, link_ids=link_ids)
        metric_names = list(SupportedTraceMetric.get_keys())
        metrics = metrics_manager.eval(metric_names)
        print("Metrics")
        print(metrics)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    @staticmethod
    def create_artifact_map(artifact_df: pd.DataFrame):
        """
        Creates map of artifact id to content.
        :param artifact_df: The data frame of artifacts.
        :return: Map of artifact id to content.
        """
        artifact_map = {}
        for artifact_index, artifact_row in artifact_df.iterrows():
            artifact_map[artifact_index] = artifact_row[ArtifactKeys.CONTENT.value]
        return artifact_map

    @staticmethod
    def parse_ranking_response(target: str, target_entries: List[TracePredictionEntry], ranked_source_ids: List[str]):
        source2labels = {entry["source"]: entry["label"] for entry in target_entries}
        scores = TracingJob.assign_scores_to_targets(ranked_source_ids)
        source_predicted_entries = []
        for source, score in zip(ranked_source_ids, scores):
            entry = {
                "source": source,
                "target": target,
                "score": score,
                "label": source2labels[source]
            }
            source_predicted_entries.append(entry)
        return source_predicted_entries

    @staticmethod
    def create_id_to_entries(entries, artifact_key: str):
        id2entries: Dict[str, List[Dict]] = {}
        for entry in entries:
            artifact_id = entry[artifact_key]
            if artifact_id not in id2entries:
                id2entries[artifact_id] = []
            id2entries[artifact_id].append(entry)

        id2entries = {t_id: sorted(entries, key=lambda t: t["score"], reverse=True) for t_id, entries in id2entries.items()}
        return id2entries

    @staticmethod
    def assign_scores_to_targets(ranked_targets: List[str], min_score=0.5) -> List[float]:
        return create_increment_list(len(ranked_targets), min_score=min_score)
