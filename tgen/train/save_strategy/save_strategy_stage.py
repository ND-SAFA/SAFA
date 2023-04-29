from enum import Enum


class SaveStrategyStage(Enum):
    """
    Contains the two types of stages in training.
    """
    STEP = "step"
    EPOCH = "epoch"
