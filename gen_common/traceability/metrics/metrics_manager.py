import warnings
from typing import Dict, List, Tuple, Union

import numpy as np
from evaluate import load
from scipy.special import softmax

from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.objects.trace import Trace
from gen_common.data.tdatasets.trace_matrix import TraceMatrix
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.traceability.metrics.supported_trace_metric import SupportedTraceMetric, get_metric_name, get_metric_path
from gen_common.util import DictUtil

warnings.filterwarnings('ignore')
ArtifactQuery = Dict[str, List[TraceDataFrame]]
ProjectQueries = Dict[str, ArtifactQuery]


class MetricsManager:
    """
    Calculates metrics for trace trainer.
    """

    def __init__(self, trace_df: TraceDataFrame, link_ids: List[int] = None,
                 trace_predictions: Union[np.ndarray, Tuple[np.ndarray], List] = None,
                 predicted_similarities: List[float] = None):
        """
        Constructs metrics manager with labels from trace links and scores from prediction output.
        :param trace_df: The dataframe defining the links.
        :param link_ids: The links associated with prediction output.
        :param trace_predictions: The output of a model.
        :param predicted_similarities: The similarity scores predicted
        """
        if link_ids is None:
            link_ids = trace_df.index
        n_predictions = len(predicted_similarities) if trace_predictions is None else len(trace_predictions)
        n_expected = len(trace_df)
        assert n_predictions == n_expected, f"Expected {n_expected} samples but received {n_predictions} predictions."
        scores = self.get_similarity_scores(trace_predictions) if predicted_similarities is None else predicted_similarities
        self.trace_matrix = TraceMatrix(trace_df, scores, link_ids)

    def eval(self, metric_names: List) -> Dict[str, float]:
        """
        Evaluates scores using metrics and adds to base metrics. (use this instead of Trainer.evaluation to utilize predefined metrics
        from models)
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        if metric_names is None or len(metric_names) < 1:
            return {}
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = {}
        trace_matrix_metrics = SupportedTraceMetric.get_query_metrics()
        scores = self.trace_matrix.scores
        predicted_labels = list(map(lambda p: 1 if p >= 0.5 else 0, self.trace_matrix.scores))
        labels = self.trace_matrix.labels
        supported_metrics = {e.value.name for e in SupportedTraceMetric}
        for metric_path in metric_paths:
            metric = load(metric_path, keep_in_memory=True)
            args = {"trace_matrix": self.trace_matrix} if metric.name in trace_matrix_metrics else {}
            if metric.name in supported_metrics:
                args = DictUtil.update_kwarg_values(args, scores=scores)
            metric_name = get_metric_name(metric)
            try:
                metric_result = metric.compute(predictions=predicted_labels, references=labels, **args)
            except Exception:
                logger.exception(f"Unable to compute {metric_name}")
                continue
            if isinstance(metric_result, dict):
                results.update(metric_result)
            else:
                results[metric_name] = metric_result
        return results

    def get_scores(self) -> List[float]:
        """
        :return: Returns the similarity scores of the prediction output.
        """
        return self.trace_matrix.scores

    def get_trace_predictions(self) -> List[Trace]:
        """
        Constructs trace predictions for trace matrix.
        :return: Trace predictions used in evaluation.
        """
        return self.trace_matrix.entries

    @staticmethod
    def get_similarity_scores(predictions: Union[np.ndarray, Tuple[np.ndarray]]) -> List[float]:
        """
        Transforms predictions into similarity scores.
        :param predictions: The model predictions.
        :return: List of similarity scores associated with predictions.
        """
        similarity_scores = []
        n_predictions = predictions.shape[0] if isinstance(predictions, np.ndarray) else len(predictions)
        for pred_i in range(n_predictions):
            prediction = predictions[pred_i]
            if type(prediction) is np.ndarray:
                prediction = softmax(prediction)[1]
            similarity_scores.append(prediction)
        return similarity_scores
