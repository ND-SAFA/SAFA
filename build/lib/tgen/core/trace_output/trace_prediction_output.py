from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from transformers.trainer_utils import PredictionOutput

from common_resources.data.objects.trace import Trace
from common_resources.tools.util.reflection_util import ReflectionUtil
from common_resources.tools.util.uncased_dict import UncasedDict
from tgen.core.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.stage_eval import Metrics, TracePredictions


class TracePredictionOutput(AbstractTraceOutput):
    """
    The output of predicting on the trace trainer.
    """

    def __init__(self, predictions: TracePredictions = None, label_ids: Optional[Union[np.ndarray, Tuple[np.ndarray], List]] = None,
                 metrics: Optional[Metrics] = None, source_target_pairs: List[Tuple[str, str]] = None,
                 prediction_entries: List[Trace] = None,
                 prediction_output: PredictionOutput = None,
                 original_response: List[str] = None,
                 additional_output: Dict = None):
        """
        Initializes the output with the various outputs from predictions
        :param predictions: List of 2-dimensional arrays representing similarity between each source-artifact pair.
        :param label_ids: The label associated with each prediction.
        :param metrics: Mapping between metric name and its value for predictions.
        :param source_target_pairs: List of tuples containing the source and target artifact ids for each prediction.
        :param prediction_entries: List containing source artifact, target artifact, and similarity score between them.
        :param prediction_output: The output of the prediction job.
        :param additional_output: Any additional output to store alongside the prediction output.
        :param original_response: The original responses to the prediction job.
        """
        self.original_response = original_response
        self.predictions: TracePredictions = predictions
        self.label_ids = label_ids
        metrics = {} if metrics is None else metrics
        self.metrics = UncasedDict(metrics) if not isinstance(metrics, UncasedDict) else metrics
        self.source_target_pairs = source_target_pairs
        self.prediction_entries = prediction_entries
        super().__init__(hf_output=prediction_output)
        self.set_prediction_entries()
        self.additional_output = additional_output

    def set_prediction_entries(self) -> None:
        """
        Generates the predictions for each target pair and stores them in prediction entries.
        :return: None
        """
        if self.predictions is None or self.source_target_pairs is None:
            return

        self.prediction_entries = [Trace(source=pred_ids[0], target=pred_ids[1], score=float(pred_scores))
                                   for pred_ids, pred_scores in zip(self.source_target_pairs, self.predictions)]

    def is_better_than(self, other: "TracePredictionOutput", comparison_criterion: ComparisonCriterion = None) -> bool:
        """
        Evaluates whether this result is better than the other result
        :param other: the other result
        :param comparison_criterion: The criterion used to determine best job.
        :return: True if this result is better than the other result else False
        """
        if comparison_criterion is None:
            comparison_criterion = ComparisonCriterion(metrics=[])
        assert len(comparison_criterion.metrics) <= 1, "Expected no more than 1 metric in comparison criterion."
        comparison_metric = comparison_criterion.metrics[0] if len(comparison_criterion.metrics) > 0 else None
        self_val, other_val = self._get_comparison_vals(other, comparison_metric)
        if self_val is None or other_val is None:
            return False
        result = comparison_criterion.comparison_function(self_val, other_val)
        return result

    def _can_compare_with_metric(self, other: "TracePredictionOutput", comparison_metric_name: str) -> bool:
        """
         Returns True if can use comparison metric to compare the two results
         :param other: other result
         :param comparison_metric_name: The metric used to compare which is the best prediction output.
         :return: True if can use comparison metric to compare the two results else false
         """
        if not comparison_metric_name:
            return False
        if self.metrics and other.metrics:
            if comparison_metric_name in self.metrics and comparison_metric_name in other.metrics:
                return True
        return False

    def _get_comparison_vals(self, other: "TracePredictionOutput", comparison_metric_name: str) -> Tuple:
        """
        Gets the values to use for comparison
        :param other: the other result
        :param comparison_metric_name: The metric used to compare which is the best prediction output.
        :return: the values to use for comparison
        """
        if self._can_compare_with_metric(other, comparison_metric_name):
            return self.metrics[comparison_metric_name], other.metrics[comparison_metric_name]
        return None, None

    def to_json(self) -> Dict:
        """
        Converts the output to json
        :return: The output as a dictionary
        """
        return ReflectionUtil.get_fields(self)
