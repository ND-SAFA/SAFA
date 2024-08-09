from typing import List, Type

from sklearn.metrics import average_precision_score

from tgen_test.train.metrics.test_metric_at_k import TestMetricAtK
from tgen.metrics.abstract_trace_metric import AbstractTraceMetric
from tgen.metrics.map_at_k_metric import MapAtKMetric


class TestMapAtK(TestMetricAtK):
    """
    Tests that MAP at k correctly identifies the correct k elements and applies the
    correct metric to them.
    ---
        Predictions: 0.6, .9, .7
        Labels: 1, 0, 1
        PrecisionAtK: Sort by similarity score, get top k, evaluate precision. [(0.9, 0), (0.7, 1), (0.6, 1)]
        Precision: tp / tp + fp
    ---
        Note, sklearn treats no predictions as having 100% precision, if positive class exists
        If k = 1 -> thresholds [<=0.9, >.9]-> precisions [0, 0] -> avg = 0
        If k = 1 -> thresholds [.7, .9]  -> precisions [0.5, 0, 1] -> avg = 0.5
        If k = 3 -> thresholds [.6, .7, .9]-> TODO
        If k = 3 then 1 / (2 + 1) = 1 / 3 = .66
    """

    def test_correctness(self):
        self.assert_construction()
        self.assert_correctness()

    @property
    def base_metric_name(self) -> str:
        return "map"

    @property
    def metric_class(self) -> Type[AbstractTraceMetric]:
        return MapAtKMetric

    @property
    def expected_metric_scores(self) -> List[float]:
        return [0,
                average_precision_score([0, 1], [.9, .7]),
                average_precision_score([0, 1, 1], [.9, .7, .6])]
