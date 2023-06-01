import random
from collections import namedtuple
from copy import deepcopy
from typing import Callable, Iterable, List, Union

import numpy as np
from tqdm import tqdm

from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.util.enum_util import EnumDict

Query = namedtuple('Query', ['links', 'preds'])


class TraceMatrix:
    """
    Contains trace and similarity matrices for computing query-based metrics.
    """

    def __init__(self, trace_df: TraceDataFrame, predicted_scores: Union[List[float], np.ndarray] = None, link_ids: List[int] = None,
                 randomize: bool = False):
        """
        Constructs similarity and trace matrices using predictions output.
        :param trace_df: The dataframe of trace links.
        :param predicted_scores: The prediction scores on the links.
        :param link_ids: If provided, specifies the order of the predicted_scores
        :param randomize: if True, randomizes the order of links in the matrix
        """
        self.query_matrix = {}
        self.source_ids = []
        self.labels = []
        self.entries = []
        self.scores = predicted_scores
        self._fill_trace_matrix(trace_df, predicted_scores, link_ids)
        if randomize:
            self._do_randomize()

    def calculate_query_metric(self, metric: Callable[[List[int], List[float]], float], default_value: float = None):
        """
        Calculates the average metric for each source artifact in project.
        :param metric: The metric to compute for each query in matrix.
        :param default_value: The value to use if there are no valid metric scores.
        :return: Average metric value.
        """
        metric_values = []
        for source, query in self.query_matrix.items():
            query_predictions = query.preds
            query_labels = [link[TraceKeys.LABEL] for link in query.links]
            query_metric = metric(query_labels, query_predictions)
            if not np.isnan(query_metric):
                metric_values.append(query_metric)
        if len(metric_values) == 0:
            return default_value
        return sum(metric_values) / len(metric_values)

    def calculate_query_metric_at_k(self, metric: Callable[[List[int], List[float]], float], k: int, **kwargs):
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

        return self.calculate_query_metric(metric_at_k, **kwargs)

    def _fill_trace_matrix(self, trace_df: TraceDataFrame, predicted_scores: List[float] = None, link_ids: List[int] = None) -> None:
        """
        Adds all links to the map between source artifacts and their associated trace links.
        :param trace_df: The dataframe of trace links.
        :param predicted_scores: the list of similarity scores for each link
        :param link_ids: If provided, specifies the order of the predicted_scores
        :return: None
        """
        link_ids = trace_df.index if link_ids is None else link_ids
        predicted_scores = [None for link in range(len(link_ids))] if predicted_scores is None else predicted_scores
        for i, link_id in tqdm(enumerate(link_ids), desc="Filling trace matrix", total=len(link_ids)):
            link = trace_df.get_link(link_id)
            self.add_link(link, predicted_scores[i])

    def add_link(self, link: EnumDict, pred: float = None) -> None:
        """
        Adds a new link to the trace matrix
        :param link: the trace link
        :param pred: the prediction associated with the link
        :return: None
        """
        if link[TraceKeys.SOURCE] not in self.query_matrix:
            self.query_matrix[link[TraceKeys.SOURCE]] = Query(links=[], preds=[])
            self.source_ids.append(link[TraceKeys.SOURCE])
        self.query_matrix[link[TraceKeys.SOURCE]].links.append(link)
        self.labels.append(link[TraceKeys.LABEL])
        self.entries.append({"source": link[TraceKeys.SOURCE], "target": link[TraceKeys.TARGET]})
        if pred is not None:
            self.query_matrix[link[TraceKeys.SOURCE]].preds.append(pred)

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
