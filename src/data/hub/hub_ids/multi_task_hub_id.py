from abc import ABC

from data.hub.abstract_hub_id import AbstractHubId


class MultiTaskHubId(AbstractHubId, ABC):
    """
    Provides base implementation for managing different tasks with different splits all from the same source file.
    """

    def __init__(self, task: str, stage: str):
        """
        Initialized hub for given task at given stage.
        :param task: The type of task defined by this dataset.
        :param stage: The stage of the splits (e.g. train, val, eval).
        """
        self.task = task
        self.stage = stage
