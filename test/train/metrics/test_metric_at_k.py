from abc import ABC, abstractmethod
from typing import List, Type

import numpy as np

from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.tdatasets.trace_matrix import TraceMatrix
from tgen.testres.base_tests.base_test import BaseTest
from tgen.train.metrics.abstract_trace_metric import AbstractTraceMetric


class TestMetricAtK(BaseTest, ABC):
    """
    Tests the correctness of a metric calculated per top k results per query.
    """
    SOURCE_PREFIX = "S"
    TARGET_PREFIX = "T"
    n_sources = 1
    n_targets = 3
    predictions = np.array([0.6, 0.9, 0.7])
    labels = np.array([1, 0, 1])

    def assert_correctness(self):
        metric = self.metric_class()
        prefix = (self.SOURCE_PREFIX, self.TARGET_PREFIX)
        n_artifacts = (self.n_sources, self.n_targets)
        trace_links = self.create_trace_links(prefix, n_artifacts, self.labels)
        trace_matrix = TraceMatrix(trace_links, self.predictions)
        metric_results = metric._compute(self.predictions, self.labels, trace_matrix)
        for i, expected_score in enumerate(self.expected_metric_scores):
            metric_name = self.metric_name + "@%s" % (str(i + 1))
            self.assertAlmostEqual(expected_score, metric_results[metric_name], msg="Failed:" + metric_name, delta=0.01)

    def assert_construction(self):
        """
        That that trace links are constructed according to requirements.
        :return:
        :rtype:
        """
        prefix = (self.SOURCE_PREFIX, self.TARGET_PREFIX)
        n_artifacts = (self.n_sources, self.n_targets)
        trace_links = self.create_trace_links(prefix, n_artifacts, self.labels)
        targets = [self.TARGET_PREFIX + str(i) for i in range(self.n_targets)]
        i = 0
        for _, trace_link in trace_links.iterrows():
            self.assertEqual(trace_link[TraceKeys.SOURCE.value], "S0")
            self.assertEqual(trace_link[TraceKeys.TARGET.value], targets[i])
            self.assertEqual(trace_link[TraceKeys.LABEL.value], self.labels[i])
            i += 1

    @property
    @abstractmethod
    def metric_name(self) -> str:
        """
        :return: Returns the expected metric name used to query metric results
        """

    @property
    @abstractmethod
    def metric_class(self) -> Type[AbstractTraceMetric]:
        """
        :return: Returns the expected metric name used to query metric results
        """

    @property
    @abstractmethod
    def expected_metric_scores(self) -> List[float]:
        """
        :return: Returns the expected metric scores per k in increasing order (e.g. 1,2,3)
        """
