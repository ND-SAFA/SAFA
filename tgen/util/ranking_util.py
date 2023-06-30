import json
from typing import Dict, List

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.ranking.pipeline.artifact_ranking_step import ArtifactRankingStep
from tgen.ranking.pipeline.base import RankingStore
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.util.logging.logger_manager import logger


class RankingUtil:
    """
    Contains utility methods for dealing with artifact layers.
    """

    @staticmethod
    def rank_children(parent_ids: List[str], parent2children: Dict[str, List[str]], artifact_map: Dict[str, str]):
        ranking_store = RankingStore()
        ranking_store.artifact_map = artifact_map
        ranking_store.parent_ids = parent_ids  # flip flop because in study source = target
        ranking_store.parent2children = parent2children
        ranking_step = ArtifactRankingStep()
        ranking_step(ranking_store)
        batched_ranked_children = ranking_store.processed_ranking_response
        return batched_ranked_children

    @staticmethod
    def get_parent_child_types(artifact_df: ArtifactDataFrame):
        """
        Returns the artifacts types of the parent and child artifacts.
        :param artifact_df: The data frame of artifacts.
        :return: Parent type and child type.
        """

        counts_df = artifact_df[ArtifactKeys.LAYER_ID].value_counts()
        if len(counts_df) > 2:
            raise NotImplementedError("Multi-layer tracing is under construction.")
        n_sources = min(counts_df)
        parent_type = counts_df[counts_df == n_sources].index[0]
        child_type = counts_df[counts_df != n_sources].index[0]
        return parent_type, child_type

    @staticmethod
    def parse_ranking_response(parent_id: str, ranked_children_ids: List[str], children_entries: List[TracePredictionEntry] = None):
        children2label = {entry["source"]: entry["label"] for entry in children_entries} if children_entries else {}
        scores = RankingUtil.assign_scores_to_targets(ranked_children_ids)
        predicted_entries = []
        for child_id, score in zip(ranked_children_ids, scores):
            label = children2label.get(child_id, None)
            entry = {
                "source": child_id,
                "target": parent_id,
                "score": score,
                "label": label
            }
            predicted_entries.append(entry)
        return predicted_entries

    @staticmethod
    def assign_scores_to_targets(ranked_targets: List[str], min_score=0.5) -> List[float]:
        return RankingUtil.create_increment_list(len(ranked_targets), min_score=min_score)

    @staticmethod
    def create_increment_list(n: int, max_score=1.0, min_score=0.0):
        increment = (max_score - min_score) / (n - 1)  # Calculate the increment between numbers
        descending_list = [max_score - i * increment for i in range(n)]  # Generate the descending list
        return descending_list

    @staticmethod
    def calculate_ranking_metrics(dataset: TraceDataset, predicted_entries: List[TracePredictionEntry]):
        n_labels = len(dataset.trace_df[TraceKeys.LABEL].unique())
        if n_labels > 1:
            link_ids = [TraceDataFrame.generate_link_id(entry["source"], entry["target"]) for entry in predicted_entries]
            scores = [entry["score"] for entry in predicted_entries]
            trace_df = dataset.trace_df.filter_by_index(link_ids)

            metrics_manager = MetricsManager(trace_df, predicted_similarities=scores, link_ids=link_ids)
            metric_names = list(SupportedTraceMetric.get_keys())
            metrics = metrics_manager.eval(metric_names)
            logger.log_with_title("Metrics", json.dumps(metrics, indent=4))
            return metrics
