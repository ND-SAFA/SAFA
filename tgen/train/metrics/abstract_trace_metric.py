from abc import ABC, abstractmethod

import datasets
from datasets import MetricInfo

from util.base_object import BaseObject


class AbstractTraceMetric(datasets.Metric, BaseObject, ABC):

    @abstractmethod
    def _info(self) -> MetricInfo:
        pass

    def get_features(self) -> datasets.Features:
        """
        Gets the features for the metric
        :return: the features
        """
        return datasets.Features(
            {
                "predictions": datasets.Sequence(datasets.Value("float32")),
                "references": datasets.Sequence(datasets.Value("int32")),
            }
            if self.config_name == "multilabel"
            else {
                "predictions": datasets.Value("float32"),
                "references": datasets.Value("int32"),
            }
        )
