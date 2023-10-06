import json
from typing import Dict, List, Optional, Tuple

from tgen.common.constants.tracing.ranking_constants import TIER_ONE_THRESHOLD, TIER_TWO_THRESHOLD
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.list_util import ListUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.tracing.ranking.common.tracing_request import TracingRequest


class RankingUtil:
    """
    Contains utility methods for dealing with artifact layers.
    """
    @staticmethod
    def evaluate_trace_predictions(trace_df: TraceDataFrame, predicted_entries: List[EnumDict]) -> Optional[Dict]:
        """
        Calculates ranking metrics for ranking predictions.
        :param trace_df: The trace data frame containing true labels.
        :param predicted_entries: The ranking predictions.
        :return: The dictionary of metrics.
        """
        if trace_df is None:
            logger.info("Skipping evaluation, trace data frame is none.")
            return
        n_labels = len(trace_df[TraceKeys.LABEL].unique())
        if n_labels == 0:
            logger.info("Skipping evaluation, no labels found in trace data frame.")
            return
        if not isinstance(predicted_entries[0], EnumDict):
            predicted_entries = [EnumDict(e) for e in predicted_entries]

        all_link_ids = list(trace_df.index)
        positive_link_ids = [t[TraceKeys.LINK_ID] for t in trace_df.get_links_with_label(1)]
        negative_link_ids = [t[TraceKeys.LINK_ID] for t in trace_df.get_links_with_label(0)]
        predicted_link_ids = [TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE], entry[TraceKeys.TARGET]) for
                              entry in predicted_entries]
        predicted_t_map = {t_id: t for t_id, t in zip(predicted_link_ids, predicted_entries)}

        false_negative_ids = list(set(positive_link_ids).difference(set(predicted_link_ids)))
        false_positive_ids = list(set(negative_link_ids).intersection(set(predicted_link_ids)))

        RankingUtil.log_artifacts("False Negatives", trace_df.to_map(), false_negative_ids)
        RankingUtil.log_artifacts("False Positives", predicted_t_map, false_positive_ids)

        other_link_ids = set(all_link_ids).difference(predicted_link_ids)
        ordered_link_ids = predicted_link_ids + list(other_link_ids)
        scores = [entry[TraceKeys.SCORE.value] for entry in predicted_entries]
        missing_scores = [0 for i in other_link_ids]
        all_scores = scores + missing_scores

        metrics_manager = MetricsManager(trace_df, predicted_similarities=all_scores, link_ids=ordered_link_ids)
        metric_names = list(SupportedTraceMetric.get_keys())
        metrics = metrics_manager.eval(metric_names)
        logger.log_with_title("Ranking Metrics", json.dumps(metrics))
        return metrics

    @staticmethod
    def ranking_to_predictions(parent2rankings, parent2explanations: Dict[str, List[str]] = None) -> List[Trace]:
        """
        Converts ranking to prediction entries.
        :param parent2rankings: Mapping of parent name to ranked children.
        :param parent2explanations: Dictionary mapping the parent to a list of explanations for each child prediction
        :return: List of prediction entries.
        """
        predicted_entries = []
        for parent_id, ranked_children in parent2rankings.items():
            if isinstance(ranked_children, tuple):
                ranked_children, children_scores = ranked_children
            else:
                children_scores = ListUtil.create_step_list(len(ranked_children))

            explanations = parent2explanations[parent_id] if parent2explanations else None
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_children, scores=children_scores,
                                                                              explanations=explanations)
            predicted_entries.extend(target_predicted_entries)
        return predicted_entries

    @staticmethod
    def create_ranking_predictions(parent_id: str, ranked_children_ids: List[str],
                                   scores: List[float] = None, original_entries: List[Trace] = None,
                                   explanations: List[str] = None) -> List[Trace]:
        """
        Creates ranking predictions by assigning scores to ranking in linear fashion.
        :param parent_id: The parent artifact id.
        :param ranked_children_ids: The ranked children for parent.
        :param scores: The list of scores for each child prediction.
        :param original_entries: The original entries to extract labels from.
        :param explanations: A list of explanations for each child prediction.
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
    def log_artifacts(title: str, trace_map: Dict, artifact_ids: List[str], group_key: str = TraceKeys.TARGET.value) -> None:
        """
        Logs the missing links (false negatives).
        :param title: The title to use when logging
        :param trace_map: The trace data mapping id to trace dict
        :param artifact_ids: The IDs of the missing links.
        :param group_key: The key used to group missing ids (either by parent or child).
        :return: None
        """
        artifact_id_key = TraceKeys.SOURCE.value if group_key == TraceKeys.TARGET.value else TraceKeys.TARGET.value

        missing_links = [trace_map[t_id] for t_id in artifact_ids]
        grouped_links = RankingUtil.group_trace_predictions(missing_links, group_key)
        grouped_links = {g: [RankingUtil.format_link(link, artifact_id_key) for link in g_links] for g, g_links in
                         grouped_links.items()}
        logger.log_title(title)
        for group_key, group_items in grouped_links.items():
            logger.info(f"{group_key}:{group_items}")

    @staticmethod
    def select_predictions(trace_predictions: List[Trace]) -> List[Trace]:
        """
        Selects the top parents per child.
        :param trace_predictions: The trace predictions.
        :return: List of selected predictions.
        """
        children2entry = RankingUtil.group_trace_predictions(trace_predictions, TraceKeys.child_label().value)
        predictions = []

        for child, child_predictions in children2entry.items():
            sorted_entries = sorted(child_predictions, key=lambda e: e[TraceKeys.SCORE.value], reverse=True)
            t1_preds, t2_preds, t3_preds = [], [], []

            t1_preds = [s for s in sorted_entries if s[TraceKeys.SCORE.value] >= TIER_ONE_THRESHOLD]
            t2_preds = [s for s in sorted_entries if TIER_TWO_THRESHOLD <= s[TraceKeys.SCORE.value] < TIER_ONE_THRESHOLD]
            t3_preds = t3_preds if len(t1_preds) + len(t2_preds) > 0 else sorted_entries[:1]
            if len(t1_preds) > 0:
                selected_entries = t1_preds
            elif len(t2_preds):
                selected_entries = t2_preds
            else:
                selected_entries = t3_preds

            predictions.extend(selected_entries)

        return predictions

    @staticmethod
    def group_trace_predictions(predictions: List[Trace], key_id: str):
        """
        Groups the predictions by the property given.
        :param predictions: The predictions to group.
        :param key_id: The id of the key to access the child from the entry
        :return: Dictionary of keys in key_id and their associated entries.
        """
        children2entry = {}
        for entry in predictions:
            child_id = entry[key_id]
            if child_id not in children2entry:
                children2entry[child_id] = []
            children2entry[child_id].append(entry)
        return children2entry

    @staticmethod
    def format_link(a: Dict, artifact_id_key: str):
        """
        Formats the artifact with its score and explanation if it exists.
        :param a: The artifact to format.
        :param artifact_id_key: The key to get the id of the artifact to display.
        :return: Formatted string.
        """
        a_id = a[artifact_id_key]
        a_score = a.get(TraceKeys.SCORE.value)
        return f"{a_id}: ({a_score})"

    @staticmethod
    def extract_tracing_requests(artifact_df: ArtifactDataFrame, layers: List[Tuple[str, str]]) -> List[TracingRequest]:
        """
        Extracts source and target artifact names for each layer
        :param artifact_df: Artifact data frame containing ids, bodies, and types.
        :param layers: The layers being traced, containing list of (child, parent) tuples.
        :return:
        """
        requests = []
        artifact_map = artifact_df.to_map()
        for child_type, parent_type in layers:
            parent_df = artifact_df.get_type(parent_type)
            child_df = artifact_df.get_type(child_type)

            parent_names = list(parent_df.index)
            child_names = list(child_df.index)
            requests.append(TracingRequest(child_ids=child_names, parent_ids=parent_names, artifact_map=artifact_map))
        return requests

    @staticmethod
    def create_entry(parent: str, child: str, score: float = 0.0) -> EnumDict:
        """
        Creates a prediction entry
        :param parent: The parent artifact id
        :param child: The child artifact id
        :param score: The score representing strength of link between child + parent
        :return: a prediction entry
        """
        return EnumDict({
            TraceKeys.parent_label(): parent,
            TraceKeys.child_label(): child,
            TraceKeys.SCORE: score
        })

    @staticmethod
    def convert_parent2rankings_to_prediction_entries(parent2rankings: Dict[str, List]) -> Dict[str, List[EnumDict]]:
        """
        Converts the parent2ranking dictionary produced by the sorters into a list of prediction entries
        :param parent2rankings: The dictionary produced by the sorter containing parent art id mapped to ordered children
        :return: A list of enum dictionaries representing a prediction entry for each parent, child pair
        """
        prediction_entries = {}
        for parent, parent_payload in parent2rankings.items():
            prediction_entries[parent] = []
            for child, score in zip(*parent_payload):
                entry = RankingUtil.create_entry(parent, child, score)
                prediction_entries[parent].append(entry)
        return prediction_entries
