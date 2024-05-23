from trace import Trace
from typing import Dict, List, Tuple

from sklearn.metrics import average_precision_score

from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.trace_matrix import TraceMatrix
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric


class TracingEvaluator:
    def __init__(self, trace_df: TraceDataFrame, predictions: List[Trace] = None):
        """
        Creates a new TracingEvaluator for given predictions on trace data frame.
        :param trace_df:
        :param predictions:
        """
        if predictions is None:
            assert not trace_df[TraceKeys.SCORE].isna().all(), "Expected scores to be inside of trace data frame."
        self.traces = [t for i, t in trace_df.itertuples()]
        self.predictions = predictions
        self.query_label = TraceKeys.parent_label()
        self.other_label = TraceKeys.child_label() if self.query_label == TraceKeys.parent_label() else TraceKeys.child_label()
        self._set_scores()

    def calculate_metrics(self) -> Tuple[Dict, Dict]:
        trace_df, scores = self.get_trace_inputs()
        metrics_manager = MetricsManager(trace_df, predicted_similarities=scores)
        metrics = metrics_manager.eval(SupportedTraceMetric.get_keys())

        query_metrics = sorted(self.calculate_query_metrics(), key=lambda t: t["ap"])
        return metrics, query_metrics

    def calculate_query_metrics(self) -> List[Dict]:
        trace_df, scores = self.get_trace_inputs()
        trace_matrix = TraceMatrix(trace_df, scores)

        global_query_metrics = []
        for query_id, query in trace_matrix.query_matrix.items():
            query_predictions = query.links
            query_labels = [q[TraceKeys.LABEL] for q in query_predictions]
            query_scores = [q[TraceKeys.SCORE] for q in query_predictions]
            sorted_predictions = sorted(query_predictions, key=lambda t: t[TraceKeys.SCORE], reverse=True)
            trace_locations = [i for i, t in enumerate(sorted_predictions) if t[TraceKeys.LABEL] == 1]
            query_metrics = {
                "query_id": query_id,
                "ap": average_precision_score(query_labels, query_scores),
                "n_traces": len(trace_locations),
            }

            if len(trace_locations) > 0:
                top_trace_loc = min(trace_locations)
                top_trace = query_predictions[top_trace_loc]
                query_metrics.update({
                    "top_trace": top_trace[self.other_label],
                    "top_trace_loc": top_trace_loc,
                    "top_trace_score": top_trace[TraceKeys.SCORE],
                })
                bottom_trace_loc = max(trace_locations)
                bottom_trace_thresh = query_predictions[bottom_trace_loc][TraceKeys.SCORE]
                false_positives = [q[self.other_label] for q in query_predictions if q[TraceKeys.SCORE] >= bottom_trace_thresh]
                query_metrics.update({
                    "false positives": false_positives
                })

            if len(trace_locations) > 1:
                bottom_trace_loc = max(trace_locations)
                bottom_trace = query_predictions[bottom_trace_loc]
                query_metrics.update({
                    "bottom_trace": bottom_trace[self.other_label],
                    "bottom_trace_loc": bottom_trace_loc,
                    "bottom_trace_score": bottom_trace[TraceKeys.SCORE]
                })

            global_query_metrics.append(query_metrics)
        return global_query_metrics

    def _set_scores(self) -> None:
        """
        Calculates list of scores ordered by trace df index.
        :return:
        """
        prediction_map = {}
        for entry in self.predictions:
            prediction_map[entry[TraceKeys.LINK_ID]] = entry
        scores = []
        for t in self.traces:
            t_id = t[TraceKeys.LINK_ID]
            score = prediction_map[t_id][TraceKeys.SCORE] if t_id in prediction_map else 0
            t[TraceKeys.SCORE] = score

    def get_trace_inputs(self) -> Tuple[TraceDataFrame, List[float]]:
        """
        :return: Returns common inputs for tracing components.
        """
        trace_df = TraceDataFrame(self.traces)
        scores = list(trace_df[TraceKeys.SCORE])
        return trace_df, scores
