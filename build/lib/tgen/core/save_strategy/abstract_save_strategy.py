from abc import ABC, abstractmethod
from typing import Any, Callable, Dict

from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.enum_util import FunctionalWrapper
from common_resources.tools.util.supported_enum import SupportedEnum
from tgen.core.save_strategy.save_strategy_stage import SaveStrategyStage
from tgen.core.trace_output.stage_eval import Metrics

ComparisonFunction = Callable[[Any, Any], bool]


class SupportedComparisonFunction(SupportedEnum):
    """
    Represents the different ways to compare metrics scores.
    Note, this is not an enum because functional wrapper break deepcopy method.
    """
    MAX = FunctionalWrapper(lambda a, b: b is None or a > b)
    MIN = FunctionalWrapper(lambda a, b: b is None or a < b)


class AbstractSaveStrategy(BaseObject, ABC):
    """
    Defines the strategy for deciding
    """

    def __init__(self):
        """
        Constructs save strategy with empty evaluations.
        """
        self.stage_evaluations: Dict[int, Metrics] = {}

    @abstractmethod
    def should_evaluate(self, stage: SaveStrategyStage, stage_iteration: int) -> bool:
        """
        Returns whether model should be evaluated during this step.
        :param stage: Whether step or epoch has been performed.
        :param stage_iteration: The number of iterations on stage.
        :return: Whether the training loop should evaluate model.
        """

    @abstractmethod
    def should_save(self, metrics: Metrics, id: int) -> bool:
        """
        Returns whether current model state should be saved.
        :param metrics: The results of evaluating the model.
        :param id: The id of the evaluation result.
        :return: True if model should be saved otherwise false.
        """
        self.stage_evaluations[id] = metrics
