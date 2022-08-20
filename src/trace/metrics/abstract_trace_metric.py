from typing import Dict, List, re

import datasets
from abc import abstractmethod, ABC


class AbstractTraceMetric(datasets.Metric, ABC):
    metric_suffix = "Metric"

    def get_features(self) -> datasets.Features:
        """
        Gets the features for the metric
        :return: the features
        """
        return datasets.Features(
            {
                "predictions": datasets.Sequence(datasets.Value("int32")),
                "references": datasets.Sequence(datasets.Value("int32")),
            }
            if self.config_name == "multilabel"
            else {
                "predictions": datasets.Value("int32"),
                "references": datasets.Value("int32"),
            }
        )

    @abstractmethod
    def _perform_compute(self, predictions: List, labels: List, **kwargs) -> float:
        """
        Helper method to perform computations specific to metric
        :param predictions: the predictions
        :param labels: the true labels
        :param kwargs: any other arguments used in computation
        :return: the score
        """
        pass

    def _compute(self, predictions: List, references: List, **kwargs) -> Dict:
        """
        Performs the computation
        :param predictions: the predictions
        :param references: the true labels
        :param kwargs: any other arguments used in computation
        :return: metric name, score mappings
        """
        return {
            self.metric_name: self._perform_compute(predictions, references, **kwargs)
        }
