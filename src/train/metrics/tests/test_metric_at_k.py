from abc import ABC, abstractmethod
from typing import List, Type

import numpy as np

from data.datasets.trace_matrix import TraceMatrixManager
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from testres.base_test import BaseTest
from train.metrics.abstract_trace_metric import AbstractTraceMetric


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
        trace_links = self.create_trace_links()
        trace_matrix = TraceMatrixManager(trace_links, self.predictions)
        metric_results = metric._compute(self.predictions, self.labels, trace_matrix)
        for i, expected_score in enumerate(self.expected_metric_scores):
            metric_name = self.metric_name + "@%s" % (str(i + 1))
            self.assertAlmostEqual(metric_results[metric_name], expected_score, msg="Failed:" + metric_name)

    def assert_construction(self):
        """
        That that trace links are constructed according to requirements.
        :return:
        :rtype:
        """
        trace_links = self.create_trace_links()
        targets = [self.TARGET_PREFIX + str(i) for i in range(self.n_targets)]
        for i, trace_link in enumerate(trace_links):
            self.assertEqual(trace_link.source.id, "S0")
            self.assertEqual(trace_link.target.id, targets[i])
            self.assertEqual(trace_link.is_true_link, self.labels[i] == 1)

    def create_trace_links(self):
        """
        Creates trace links between source and targets.
        :return: Trace links constructed defined by n_sources and n_targets.
        """

        source_artifacts = self.create_artifacts(self.SOURCE_PREFIX, self.n_sources)
        target_artifacts = self.create_artifacts(self.TARGET_PREFIX, self.n_targets)
        trace_links = []
        label_index = 0
        for source_artifact in source_artifacts:
            for target_artifact in target_artifacts:
                is_true_link = self.labels[label_index] == 1
                trace_links.append(TraceLink(source_artifact, target_artifact, is_true_link))
                label_index += 1
        return trace_links

    @staticmethod
    def create_artifacts(prefix: str, n_artifacts: int, body: str = "body"):
        """
        Creates list of artifacts whose id contain prefix.
        :param prefix: The prefix to name artifact with.
        :param n_artifacts: The number of artifacts to create.
        :param body: The artifact body to supply artifacts with.
        :return: List of artifacts created.
        """
        return [Artifact(prefix + str(i), body) for i in range(n_artifacts)]

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
