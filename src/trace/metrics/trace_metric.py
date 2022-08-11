from typing import Dict, List

from datasets import Metric
from abc import ABC, abstractmethod
import os
from common.config.paths import PROJ_PATH


class TraceMetric(Metric, ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of metric
        :return: the name
        """
        pass

    @property
    def path(self) -> str:
        """
        The path to metric class file
        :return: the path
        """
        return os.path.dirname(os.path.relpath(__file__, PROJ_PATH))

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

    def _compute(self, predictions: List, references: List) -> Dict:
        """
        Performs the computation
        :param predictions: the predictions
        :param references: the true labels
        :return: metric name, score mappings
        """
        return {
            self.name: self._perform_compute(predictions, references)
        }
