from typing import List

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from common_resources.data.tdatasets.dataset_role import DatasetRole
from tgen.testres.object_creator import ObjectCreator
from common_resources.tools.variables.typed_definition_variable import TypedDefinitionVariable

EVAL_CREATOR_PARAM = "eval_dataset_creator"
VAL_CREATOR_PARAM = "val_dataset_creator"


class DatasetCreatorTUtil:

    @staticmethod
    def create_trainer_dataset_manager(additional_roles: List[DatasetRole] = None, val_percentage: float = 0.3,
                                       **kwargs) -> TrainerDatasetManager:
        """
        Creates dataset manager containing datasets in roles.
        :param additional_roles: Additional dataset roles to include.
        :param kwargs: Dictionary of properties to overwrite in dataset manager definition.
        :return: Dataset manager created.
        """
        if additional_roles is None:
            additional_roles = [DatasetRole.VAL, DatasetRole.EVAL]
        if kwargs is None:
            kwargs = {}
        trainer_dataset_manager_definition = {**kwargs}
        if DatasetRole.EVAL in additional_roles and EVAL_CREATOR_PARAM not in trainer_dataset_manager_definition:
            trainer_dataset_manager_definition[EVAL_CREATOR_PARAM] = {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            }
        if DatasetRole.VAL in additional_roles and VAL_CREATOR_PARAM not in trainer_dataset_manager_definition:
            trainer_dataset_manager_definition[VAL_CREATOR_PARAM] = {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": val_percentage
            }
        return ObjectCreator.create(TrainerDatasetManager, **trainer_dataset_manager_definition)
