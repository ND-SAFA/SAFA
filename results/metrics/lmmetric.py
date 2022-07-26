from typing import Dict

from datasets import Metric
from abc import ABC, abstractmethod
import os
from constants import PROJ_PATH


class LMMetric(Metric, ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def path(self) -> str:
        return os.path.dirname(os.path.relpath(__file__, PROJ_PATH))

    @abstractmethod
    def _perform_compute(self, predictions, labels, **kwargs) -> float:
        pass

    def _compute(self, predictions, references) -> Dict:
        """Returns the scores"""
        return {
            self.name: self._perform_compute(predictions, references)
        }
