import json
from typing import Dict, List

from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.ranking.pipeline.artifact_ranking_step import ArtifactRankingStep
from tgen.ranking.pipeline.base import RankingStore
from tgen.ranking.pipeline.sort_step import GenericSorter
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.util.logging.logger_manager import logger


class RankingUtil:
    """
    Contains utility methods for dealing with artifact layers.
    """

    @staticmethod
    def rank_children(parent_ids: List[str], parent2children: Dict[str, List[str]], artifact_map: Dict[str, str],
                      sorter: GenericSorter = None):
        if sorter:
            parent2children_sorted = {}
            for parent_id in parent_ids:
                children_ids = parent2children[parent_id]
                parent_map = sorter([parent_id], children_ids, artifact_map)
                sorted_children_ids = parent_map[parent_id]
                parent2children_sorted[parent_id] = sorted_children_ids
            parent2children = parent2children_sorted

        ranking_store = RankingStore()
        ranking_store.artifact_map = artifact_map
        ranking_store.parent_ids = parent_ids  # flip flop because in study source = target
        ranking_store.parent2children = parent2children
        ranking_step = ArtifactRankingStep()
        ranking_step(ranking_store)
        batched_ranked_children = ranking_store.processed_ranking_response
        return batched_ranked_children

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
            all_link_ids = list(dataset.trace_df.index)
            link_ids = [TraceDataFrame.generate_link_id(entry["source"], entry["target"]) for entry in predicted_entries]
            missing_ids = list(set(all_link_ids).difference(set(link_ids)))
            ordered_link_ids = link_ids + missing_ids

            scores = [entry["score"] for entry in predicted_entries]
            missing_scores = [0 for i in missing_ids]
            all_scores = scores + missing_scores

            metrics_manager = MetricsManager(dataset.trace_df, predicted_similarities=all_scores, link_ids=ordered_link_ids)
            metric_names = list(SupportedTraceMetric.get_keys())
            metrics = metrics_manager.eval(metric_names)
            logger.log_with_title("Ranking Metrics", json.dumps(metrics))
            return metrics
