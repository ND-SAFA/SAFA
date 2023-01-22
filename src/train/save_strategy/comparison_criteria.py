from dataclasses import dataclass
from typing import List, Union

from train.save_strategy.abstract_save_strategy import ComparisonFunction


@dataclass
class ComparisonCriterion:
    """
    The criterion for determining best task involving models by comparison metrics between tasks.
    """
    metrics: Union[List[str], str]
    comparison_function: Union[ComparisonFunction, str] = ComparisonFunction.MAX

    def __post_init__(self):
        if isinstance(self.metrics, str):
            self.metrics = [self.metrics]
        if isinstance(self.comparison_function, str):
            self.comparison_function = ComparisonFunction[self.comparison_function.upper()]
