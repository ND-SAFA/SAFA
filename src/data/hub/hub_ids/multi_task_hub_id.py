from abc import ABC, abstractmethod
from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from data.hub.hub_ids.task_instructions import TaskInstructions
from data.keys.structure_keys import StructuredKeys


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

    def get_definition(self) -> Dict:
        """
        :return: Returns the definition of the task initialized with.
        """
        return self.get_task_definition(self.task)

    def get_task_definition(self, task: str) -> Dict:
        """
        Returns the definition of the artifacts for given task.
        :param task: The task defined by the dataset.
        :return: Definition file content.
        """
        base_definition = self.get_base_definition()
        task_instructions = self.get_task_instructions(task)
        task_definition = StructuredKeys.create_task_definition(base_definition, task_instructions.as_update_iterator())
        return task_definition

    def get_task_instructions(self, task: str) -> TaskInstructions:
        """
        Returns the instructions for extracting definition from task.
        :param task: The task whose definition is being constructed.
        :return: 
        """
        task_map = self.get_task_instruction_map()
        if task not in task_map:
            raise ValueError(f"Unrecognized task ({task}) not one of: {task_map} ")
        artifacts = task_map[task][StructuredKeys.ARTIFACTS]
        traces = task_map[task][StructuredKeys.TRACES]
        overrides = task_map[task][StructuredKeys.OVERRIDES]
        return TaskInstructions(artifacts=artifacts, traces=traces, overrides=overrides)

    @abstractmethod
    def get_task_instruction_map(self) -> Dict:
        """
        Returns the mapping of task to its instructions.
        TODO: Structurally enforce map properties through typed dictionary or other means.
        :return: Mapping.
        """

    @abstractmethod
    def get_base_definition(self) -> Dict:
        """
        Returns the definition of the entire dataset without splitting into tasks.
        :return: Structure definition of the entire dataset.
        """
