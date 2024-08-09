from typing import List, Type

from tgen_test.train.metrics.test_metric_at_k import TestMetricAtK
from tgen.metrics.abstract_trace_metric import AbstractTraceMetric
from tgen.metrics.precision_at_threshold_metric import PrecisionAtKMetric


class TestPrecisionAtKMetric(TestMetricAtK):
    """
    Tests that precision at k correctly identifies the correct k elements and applies the
    correct metric to them.
    ---
        Predictions: 1 (0.6), 1 (0.9), 1 (0.7)
        Labels: 1, 0, 1
        PrecisionAtK: Sort by similarity score, get top k, evaluate precision. [(0.9, 0), (0.7, 1), (0.6, 1)]
        Precision: tp / tp + fp
    ---
        If k = 1 then 0 / (0 + 1) = 0 / 1 = 0
        If k = 2 then 1 / (1 + 1) = 1 / 2 = .5
        If k = 3 then 1 / (2 + 1) = 1 / 3 = .66
    """

    def test_correctness(self):
        self.assert_construction()
        self.assert_correctness()

    @property
    def metric_class(self) -> Type[AbstractTraceMetric]:
        """
        :return:Returns the precision at k metric class.
        """
        return PrecisionAtKMetric

    @property
    def base_metric_name(self):
        """
        :return: Returns the name of the precision metric within results.
        """
        return "precision"

    @property
    def expected_metric_scores(self) -> List[float]:
        """
        :return: Returns the expected metric scores per k in increasing order (e.g. 1,2,3)
        """
        return [0, 1 / 2, 2 / 3]
