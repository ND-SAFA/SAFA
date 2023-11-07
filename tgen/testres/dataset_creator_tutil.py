from typing import Dict, List

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.testres.object_creator import ObjectCreator
from tgen.variables.typed_definition_variable import TypedDefinitionVariable


class DatasetCreatorTUtil:

    @staticmethod
    def create_trainer_dataset_manager(additional_roles: List[DatasetRole] = None, kwargs: Dict = None) -> TrainerDatasetManager:
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
        if DatasetRole.EVAL in additional_roles:
            trainer_dataset_manager_definition["eval_dataset_creator"] = {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            }
        if DatasetRole.VAL in additional_roles:
            trainer_dataset_manager_definition["val_dataset_creator"] = {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": .3
            }
        return ObjectCreator.create(TrainerDatasetManager, **trainer_dataset_manager_definition)
