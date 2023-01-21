from abc import ABC, abstractmethod
from enum import Enum

from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.trace_output_types import TracePredictionOutput
from util.base_object import BaseObject


class ComparisonFunction(Enum):
    """
    Represents the different ways to compare metrics scores.
    """
    MAX = lambda a, b: b is None or a >= b
    MIN = lambda a, b: b is None or a <= b


class AbstractSaveStrategy(BaseObject, ABC):
    """
    Defines the strategy for deciding
    """

    def __init__(self):
        self.stage_evaluations = []

    @abstractmethod
    def should_evaluate(self, stage: SaveStrategyStage, stage_iteration: int) -> bool:
        """
        Returns whether model should be evaluated during this step.
        :param stage: Whether step or epoch has been performed.
        :param stage_iteration: The number of iterations on stage.
        :return: Whether the training loop should evaluate model.
        """

    @abstractmethod
    def should_save(self, evaluation_result: TracePredictionOutput) -> bool:
        """
        Returns whether current model state should be saved.
        :param evaluation_result: The results of evaluating the model.
        :return: True if model should be saved otherwise false.
        """
        self.stage_evaluations.append(evaluation_result)
