from dataclasses import dataclass
from typing import Any, Callable, List, Union

from gen_common.infra.base_object import BaseObject
from gen_common.infra.experiment.supported_comparison_function import SupportedComparisonFunction

ComparisonFunction = Callable[[Any, Any], bool]


@dataclass
class ComparisonCriterion(BaseObject):
    """
    The criterion for determining best task involving models by comparison metrics between tasks.
    """
    metrics: Union[List[str], str]
    comparison_function: Union[ComparisonFunction, str] = SupportedComparisonFunction.MAX.value

    def __post_init__(self):
        """
        Initialized single metric into list, retrieves comparison function.
        """
        if isinstance(self.metrics, str):
            self.metrics = [self.metrics]
        if isinstance(self.comparison_function, str):
            comparison_enum: SupportedComparisonFunction = getattr(SupportedComparisonFunction, self.comparison_function.upper())
            self.comparison_function = comparison_enum.value
