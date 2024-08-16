from abc import ABC, abstractmethod

import datasets
from datasets import MetricInfo
from evaluate import EvaluationModule

from gen_common.util import BaseObject


class AbstractTraceMetric(EvaluationModule, BaseObject, ABC):

    @abstractmethod
    def _info(self) -> MetricInfo:
        """
        Throws error if called. Should be implemented by child class.
        :return: None
        """
        raise Exception(f"Could not find required method `_info` on class {self.__class__.__name__}")

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
