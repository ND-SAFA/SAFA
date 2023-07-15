import json
from typing import Dict, List

from tgen.constants.tgen_constants import DEFAULT_MIN_RANKING_SCORE, DEFAULT_PARENT_MIN_THRESHOLD, DEFAULT_PARENT_THRESHOLD
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.util.list_util import ListUtil
from tgen.util.logging.logger_manager import logger


class RankingUtil:
    """
    Contains utility methods for dealing with artifact layers.
    """

    @staticmethod
    def ranking_to_predictions(parent2rankings, parent2explanations: Dict[str, List[str]]) -> List[TracePredictionEntry]:
        """
        Converts ranking to prediction entries.
        :param parent2rankings: Mapping of parent name to ranked children.
        :return: List of prediction entries.
        """
        predicted_entries = []
        for parent_id, ranked_children in parent2rankings.items():
            explanations = parent2explanations[parent_id]
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_children, explanations=explanations)
            predicted_entries.extend(target_predicted_entries)
        return predicted_entries

    @staticmethod
    def create_ranking_predictions(parent_id: str, ranked_children_ids: List[str],
                                   original_entries: List[TracePredictionEntry] = None, explanations: List[str] = None,
                                   min_score: float = DEFAULT_MIN_RANKING_SCORE) -> List[TracePredictionEntry]:
        """
        Creates ranking predictions by assigning scores to ranking in linear fashion.
        :param parent_id: The parent artifact id.
        :param ranked_children_ids: The ranked children for parent.
        :param original_entries: The original entries to extract labels from.
        :param min_score: The minimum traceability score.
        :return:
        """
        children2label = {entry["source"]: entry["label"] for entry in original_entries} if original_entries else {}
        scores = RankingUtil.assign_scores_to_targets(ranked_children_ids, min_score=min_score)
        predicted_entries = []
        for i in range(len(ranked_children_ids)):
            child_id = ranked_children_ids[i]
            score = scores[i]
            label = children2label.get(child_id, None)
            entry = {
                "source": child_id,
                "target": parent_id,
                "score": score,
                "label": label
            }
            if explanations:
                entry["explanation"] = explanations[i]
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
        return ListUtil.create_step_list(len(ranked_targets), min_score=min_score)

    @staticmethod
    def calculate_ranking_metrics(dataset: TraceDataset, ranking_entries: List[TracePredictionEntry]):
        """
        Calculates ranking metrics for ranking predictions.
        :param dataset: The original dataset used to fill any filtered out links.
        :param ranking_entries: The ranking predictions.
        :return:
        """
        if dataset.trace_df is None:
            return
        n_labels = len(dataset.trace_df[TraceKeys.LABEL].unique())
        if n_labels > 1:
            all_link_ids = list(dataset.trace_df.index)
            link_ids = [TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE.value], entry[TraceKeys.TARGET.value]) for entry in
                        ranking_entries]
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

    @staticmethod
    def select_predictions(trace_predictions: List[TracePredictionEntry],
                           parent_threshold: float = DEFAULT_PARENT_THRESHOLD,
                           min_threshold: float = DEFAULT_PARENT_MIN_THRESHOLD) -> List[TracePredictionEntry]:
        """
        Selects the top parents per child.
        :param trace_predictions: The trace predictions.
        :param parent_threshold: The minimum percentile for a child to be linked to a parent.
        :param min_threshold: The minimum threshold to consider the top prediction, if fall under parent threshold.
        :return: List of selected predictions.
        """
        children2entry = RankingUtil.group_trace_predictions(trace_predictions, TraceKeys.SOURCE.value)
        predictions = []

        for child, trace_predictions in children2entry.items():
            sorted_entries = sorted(trace_predictions, key=lambda e: e[StructuredKeys.SCORE], reverse=True)
            selected_entries = [s for s in sorted_entries if s[StructuredKeys.SCORE] >= parent_threshold]
            top_parent = sorted_entries[0]
            if len(selected_entries) == 0 and top_parent[StructuredKeys.SCORE] >= min_threshold:
                selected_entries.append(top_parent)
            predictions.extend(selected_entries)
        return predictions

    @staticmethod
    def group_trace_predictions(predictions: List[TracePredictionEntry], key_id: str):
        """
        Groups the predictions by the property given.
        :param predictions: The predictions to group.
        :return: Dictionary of keys in key_id and their associated entries.
        """
        children2entry = {}
        for entry in predictions:
            child_id = entry[key_id]
            if child_id not in children2entry:
                children2entry[child_id] = []
            children2entry[child_id].append(entry)
        return children2entry
