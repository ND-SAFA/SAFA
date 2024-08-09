from typing import List, Type

import numpy as np

from tgen_test.train.metrics.test_supported_trace_metric import TestSupportedTraceMetric
from tgen.metrics.abstract_trace_metric import AbstractTraceMetric
from tgen.metrics.specificity_metric import SpecificityMetric


class TestSpecificityMetric(TestSupportedTraceMetric):
    """
    Tests that specificity correctly identifies the correct k elements and applies the
    correct metric to them.

    TN: 2, FP: 2 SPECIFICITY = 2/4 = 0.5
    """
    predictions = np.array([0.9, 0.1, 0.8, 0.2])
    labels = np.array([0, 0, 0, 0])

    def test_correctness(self):
        self.assert_correctness()

    def assert_correctness(self):
        metric = self.metric_class()
        metric_results = metric._compute(self.predictions, self.labels)
        self.assertEqual(metric_results, 0.5)

    @property
    def metric_name(self) -> str:
        """
        :return: Returns the expected metric name used to query metric results
        """
        return "specificity"

    @property
    def metric_class(self) -> Type[AbstractTraceMetric]:
        """
        :return: Returns the expected metric name used to query metric results
        """
        return SpecificityMetric

    @property
    def expected_metric_scores(self) -> List[float]:
        """
        :return: Returns the expected metric scores per k in increasing order (e.g. 1,2,3)
        """
