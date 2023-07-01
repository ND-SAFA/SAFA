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
                      sorter: GenericSorter = None) -> Dict[str, List[str]]:
        """
        Ranks children for each parent id.
        :param parent_ids: The parent artifact ids.
        :param parent2children: Map of parent to relevant children.
        :param artifact_map: Map of artifact id to body.
        :param sorter: Sorting function to prepare children with.
        :return: Map of parent to ranked children.
        """
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
        parent2rankings = {source: ranked_children for source, ranked_children in zip(parent_ids, batched_ranked_children)}
        return parent2rankings

    @staticmethod
    def create_ranking_predictions(parent_id: str, ranked_children_ids: List[str], original_entries: List[TracePredictionEntry] = None,
                                   min_score: float = 0.5):
        """
        Creates ranking predictions by assigning scores to ranking in linear fashion.
        :param parent_id: The parent artifact id.
        :param ranked_children_ids: The ranked children for parent.
        :param original_entries: The original entries to extract labels from.
        :param min_score: The minimum traceabilty score.
        :return:
        """
        children2label = {entry["source"]: entry["label"] for entry in original_entries} if original_entries else {}
        scores = RankingUtil.assign_scores_to_targets(ranked_children_ids, min_score=min_score)
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
        """
        Assigns scores to ranked targets from 1 to min score incrementing linearly.
        :param ranked_targets: The ranked targets.
        :param min_score: The score of the last ranked artifact.
        :return: List of scores.
        """
        return RankingUtil.create_increment_list(len(ranked_targets), min_score=min_score)

    @staticmethod
    def create_increment_list(n: int, max_score=1.0, min_score=0.0):
        """
        Creates a list with scores decreasing linearly from max to min score.
        :param n: The length of the list.
        :param max_score: The score of the first item.
        :param min_score: The score of the last item.
        :return: The list of scores.
        """
        increment = (max_score - min_score) / (n - 1)  # Calculate the increment between numbers
        descending_list = [max_score - i * increment for i in range(n)]  # Generate the descending list
        return descending_list

    @staticmethod
    def calculate_ranking_metrics(dataset: TraceDataset, ranking_entries: List[TracePredictionEntry]):
        """
        Calculates ranking metrics for ranking predictions.
        :param dataset: The original dataset used to fill any filtered out links.
        :param ranking_entries: The ranking predictions.
        :return:
        """
        n_labels = len(dataset.trace_df[TraceKeys.LABEL].unique())
        if n_labels > 1:
            all_link_ids = list(dataset.trace_df.index)
            link_ids = [TraceDataFrame.generate_link_id(entry["source"], entry["target"]) for entry in ranking_entries]
            missing_ids = list(set(all_link_ids).difference(set(link_ids)))
            ordered_link_ids = link_ids + missing_ids

            scores = [entry["score"] for entry in ranking_entries]
            missing_scores = [0 for i in missing_ids]
            all_scores = scores + missing_scores

            metrics_manager = MetricsManager(dataset.trace_df, predicted_similarities=all_scores, link_ids=ordered_link_ids)
            metric_names = list(SupportedTraceMetric.get_keys())
            metrics = metrics_manager.eval(metric_names)
            logger.log_with_title("Ranking Metrics", json.dumps(metrics))
            return metrics
