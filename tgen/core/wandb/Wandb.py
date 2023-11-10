import os
from typing import Any, Dict, Tuple

import wandb

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole

GROUP_EXCLUDE = ["random_seed"]


class Wandb:
    """
    Provides utility methods for setting up run for weights and biases.
    """

    @classmethod
    def init_wandb(cls, trainer_dataset_manager: TrainerDatasetManager, model_path: str) -> None:
        """
        Initializes Weights and Biases run and configuration.
        :param trainer_dataset_manager: The dataset manager used to set the train, val, and eval names.
        :param model_name: Name of the model being trained.
        :return: None
        """
        model_name = os.path.basename(model_path)
        train_name, val_name, eval_name = Wandb.get_project_names(trainer_dataset_manager)
        run_name = f"{train_name} @ {model_name}"
        project_name = os.environ.get("WANDB_PROJECT", eval_name)
        config = {"train_project": train_name, "val_project": val_name, "eval_project": eval_name, "model": model_path}
        wandb.init(
            project=f"{project_name}",
            name=run_name,
            config=config
        )

    @classmethod
    def log(cls, role2metrics: Dict[DatasetRole, Dict]) -> None:
        """
        Logs the current metrics at given stpe prefixed with dataset role name.
        :param role2metrics: Map of role to metrics.
        :return: None
        """
        global_metrics = {}
        for dataset_role, metrics in role2metrics.items():
            named_metrics = {f"{dataset_role.name.lower()}_{k}": v for k, v in metrics.items()}
            global_metrics.update(named_metrics)
        wandb.log(global_metrics)

    @classmethod
    def finish(cls) -> None:
        """
        Finishes the wandb run.
        :return: None
        """
        wandb.finish()

    @classmethod
    def get_project_names(cls, trainer_dataset_manager: TrainerDatasetManager) -> Tuple[Any, Any, Any]:
        """
        Calculates the name of the run identifying the training, validation, and evaluation projects.
        :return: The run name
        """
        train_name = cls.get_project_name(trainer_dataset_manager, DatasetRole.TRAIN)
        eval_name = cls.get_project_name(trainer_dataset_manager, DatasetRole.EVAL)
        split_size = trainer_dataset_manager.get_split_size(DatasetRole.VAL)
        val_name = split_size if split_size else cls.get_project_name(trainer_dataset_manager, DatasetRole.VAL)
        return train_name, val_name, eval_name

    @staticmethod
    def get_project_name(trainer_dataset_creator: TrainerDatasetManager, dataset_role: DatasetRole) -> str:
        """
        Gets the name of the project associated with given role.
        :param trainer_dataset_creator: Holds the creators containing the project names.
        :param dataset_role: The role of the creator whose project name is retrieved.
        :return: The name of the project at given role.
        """
        return trainer_dataset_creator.get_creator(dataset_role).get_name()
