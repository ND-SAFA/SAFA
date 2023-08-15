import json
from typing import Dict, List

from tgen.common.util.list_util import ListUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.tgen_constants import DEFAULT_MIN_RANKING_SCORE, DEFAULT_PARENT_MIN_THRESHOLD, DEFAULT_PARENT_THRESHOLD
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric


class RankingUtil:
    """
    Contains utility methods for dealing with artifact layers.
    """

    @staticmethod
    def ranking_to_predictions(parent2rankings, parent2explanations: Dict[str, List[str]] = None) -> List[TracePredictionEntry]:
        """
        Converts ranking to prediction entries.
        :param parent2rankings: Mapping of parent name to ranked children.
        :return: List of prediction entries.
        """
        predicted_entries = []
        for parent_id, ranked_children in parent2rankings.items():
            if isinstance(ranked_children, tuple):
                ranked_children, children_scores = ranked_children
            else:
                children_scores = RankingUtil.assign_scores_to_targets(len(ranked_children))

            explanations = parent2explanations[parent_id] if parent2explanations else None
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_children, scores=children_scores,
                                                                              explanations=explanations)
            predicted_entries.extend(target_predicted_entries)
        return predicted_entries

    @staticmethod
    def create_ranking_predictions(parent_id: str, ranked_children_ids: List[str],
                                   scores: List[float] = None, original_entries: List[TracePredictionEntry] = None,
                                   explanations: List[str] = None) -> List[TracePredictionEntry]:
        """
        Creates ranking predictions by assigning scores to ranking in linear fashion.
        :param parent_id: The parent artifact id.
        :param ranked_children_ids: The ranked children for parent.
        :param original_entries: The original entries to extract labels from.
        :param min_score: The minimum traceability score.
        :return:
        """
        children2label = {entry["source"]: entry["label"] for entry in original_entries} if original_entries else {}
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
                entry[TraceKeys.EXPLANATION.value] = explanations[i]
            predicted_entries.append(entry)
        return predicted_entries

    @staticmethod
    def assign_scores_to_targets(n_items: int, min_score=DEFAULT_MIN_RANKING_SCORE) -> List[float]:
        """
        Assigns scores to ranked targets from 1 to min score incrementing linearly.
        :param n_items: The number of items to assign scores for.
        :param min_score: The score of the last ranked artifact.
        :return: List of scores.
        """
        return ListUtil.create_step_list(n_items, min_score=min_score)

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
            predicted_link_ids = [TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE.value], entry[TraceKeys.TARGET.value]) for
                                  entry in
                                  ranking_entries]
            missing_ids = list(set(all_link_ids).difference(set(predicted_link_ids)))
            ordered_link_ids = predicted_link_ids + missing_ids

            missing_links = [dataset.trace_df.get_link(t_id) for t_id in missing_ids]
            missing_links = [t for t in missing_links if t[TraceKeys.LABEL] == 1]
            missing_links = [{"parent": t[TraceKeys.TARGET],
                              "child": t[TraceKeys.SOURCE]} for t in missing_links if t[TraceKeys.LABEL] == 1]
            logger.log_with_title("Missing links", json.dumps(missing_links))

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
                           min_threshold: float = DEFAULT_PARENT_MIN_THRESHOLD,
                           top_n: int = None) -> List[TracePredictionEntry]:
        """
        Selects the top parents per child.
        :param trace_predictions: The trace predictions.
        :param parent_threshold: The minimum percentile for a child to be linked to a parent.
        :param min_threshold: The minimum threshold to consider the top prediction, if fall under parent threshold.
        :param top_n: Whether to convert scores to classification labels.
        :return: List of selected predictions.
        """
        children2entry = RankingUtil.group_trace_predictions(trace_predictions, TraceKeys.SOURCE.value)
        predictions = []

        for child, trace_predictions in children2entry.items():
            sorted_entries = sorted(trace_predictions, key=lambda e: e[StructuredKeys.SCORE], reverse=True)
            if top_n is not None:
                selected_entries = sorted_entries[:top_n]
            else:
                selected_entries = []
                t1_preds, t2_preds, t3_preds = [], [], []

                t1_preds = [s for s in sorted_entries if s[StructuredKeys.SCORE] >= 0.8]
                t2_preds = [s for s in sorted_entries if 0.7 <= s[StructuredKeys.SCORE] < 0.8]
                t3_preds = t3_preds if len(t1_preds) + len(t2_preds) > 0 else sorted_entries[:1]
                if len(t1_preds) > 0:
                    selected_entries = t1_preds
                elif len(t2_preds):
                    selected_entries = t2_preds
                else:
                    selected_entries = t3_preds

            predictions.extend(selected_entries)

        if top_n:
            for p in predictions:
                p["score"] = 1
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
