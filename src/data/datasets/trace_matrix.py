import random
from collections import namedtuple
from copy import deepcopy
from typing import Callable, Dict, Iterable, List

import numpy as np

from data.tree.trace_link import TraceLink

ArtifactQuery = Dict[str, List[TraceLink]]
ProjectQueries = Dict[str, ArtifactQuery]
Query = namedtuple('Query', ['links', 'preds'])


class TraceMatrixManager:
    """
    Contains trace and similarity matrices for computing query-based metrics.
    """

    def __init__(self, links: Iterable[TraceLink], predicted_scores: List[float] = None, randomize: bool = False):
        """
        Constructs similarity and trace matrices using predictions output.
        :param links: The list of trace links.
        :param predicted_scores: The prediction scores on the links.
        :param randomize: if True, randomizes the order of links in the matrix
        """
        self.query_matrix = {}
        self.source_ids = []
        self._fill_trace_matrix(links, [None for link in links] if predicted_scores is None else predicted_scores)
        if randomize:
            self._do_randomize()

    def add_link(self, link: TraceLink, pred: float = None) -> None:
        """
        Adds a new link to the trace matrix
        :param link: the trace link
        :param pred: the prediction associated with the link
        :return: None
        """
        if link.source.id not in self.query_matrix:
            self.query_matrix[link.source.id] = Query(links=[], preds=[])
            self.source_ids.append(link.source.id)
        self.query_matrix[link.source.id].links.append(link)
        if pred is not None:
            self.query_matrix[link.source.id].preds.append(pred)

    def calculate_query_metric(self, metric: Callable[[List[int], List[float]], float]):
        """
        Calculates the average metric for each source artifact in project.
        :param metric: The metric to compute for each query in matrix.
        :return: Average metric value.
        """
        metric_values = []
        for source, query in self.query_matrix.items():
            query_predictions = query.preds
            query_labels = [link.label for link in query.links]
            query_metric = metric(query_labels, query_predictions)
            if not np.isnan(query_metric):
                metric_values.append(query_metric)
        return sum(metric_values) / len(metric_values)

    def calculate_query_metric_at_k(self, metric: Callable[[List[int], List[float]], float], k: int):
        """
        Calculates given metric for each query considering the top k elements.
        :param metric: The metric function to apply to query scores.
        :param k: The top elements to consider.
        :return: The average of metric across queries.
        """

        def metric_at_k(query_labels: Iterable[int], query_preds: Iterable[float]):
            """
            Calculates the precision at the given k.
            :param query_labels: The labels associated with given predictions.
            :param query_preds: The predicted scores for the labels.
            :return: The metric score.
            """
            zipped = zip(query_labels, query_preds)
            results = sorted(zipped, key=lambda x: x[1], reverse=True)[:k]
            local_preds = [p for l, p in results]
            local_labels = [l for l, p in results]
            return metric(local_labels, local_preds)

        return self.calculate_query_metric(metric_at_k)

    def _fill_trace_matrix(self, links: Iterable[TraceLink], predicted_scores: List[float]) -> None:
        """
        Adds all links to the map between source artifacts and their associated trace links.
        :param links: The list of trace links.
        :param predicted_scores: the list of similarity scores for each link
        :return: None
        """
        for link, pred in zip(links, predicted_scores):
            self.add_link(link, pred)

    def _do_randomize(self) -> None:
        """
        Randomizes the order of links in the matrix and source ids.
        :return: None
        """
        random.shuffle(self.source_ids)
        for source, query in self.query_matrix.items():
            links_to_randomize = deepcopy(query.links)
            random.shuffle(links_to_randomize)
            self.query_matrix[source] = Query(links=links_to_randomize, preds=query.preds)
