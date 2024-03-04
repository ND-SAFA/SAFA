import os
from typing import Any, Dict, List, Tuple

import wandb

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.logging.logger_manager import logger
from tgen.data.tdatasets.dataset_role import DatasetRole

GROUP_EXCLUDE = ["random_seed"]
ARGS_PARAMS = ["num_train_epochs",
               "metric_for_best_model",
               "gradient_accumulation_steps",
               "st_loss_function",
               "learning_rate",
               "freeze_base",
               "use_scores"]


class WBManager:
    """
    Provides utility methods for setting up run for weights and biases.
    """
    HAS_INITIALIZED = False

    @classmethod
    def update_config(cls, obj: Dict = None, args: Any = None) -> None:
        """
        Updates the configuration of Weights and Biases run.
        :param obj: The new properties to add or override in config.
        :param args: Arguments to add to config.
        :return: None
        """
        if not cls.HAS_INITIALIZED:
            return
        if obj is None:
            obj = {}
        if args:
            args_config = cls.create_config_dict(args, ARGS_PARAMS)
            obj.update(args_config)
        wandb.config.update(obj)
        logger.info(f"Configuration Update: {obj}")

    @staticmethod
    def create_config_dict(obj: Any, props: List[str]):
        """
        Adds the properties from args to a dictionary.
        :param obj: The object to extract the properties from.
        :param props: The properties to extract.
        :return: The dictionary containing properties specified.
        """
        config = {}
        for prop in props:
            if hasattr(obj, prop) and getattr(obj, prop) is not None:
                config[prop] = getattr(obj, prop)
        return config

    @classmethod
    def init_wandb(cls, trainer_dataset_manager: "TrainerDatasetManager", model_path: str, run_suffix=None) -> None:
        """
        Initializes Weights and Biases run and configuration.
        :param trainer_dataset_manager: The dataset manager used to set the train, val, and eval names.
        :param model_path: Path to model. Accepts huggingface repo names.
        :param run_suffix: Suffix to run name.
        :return: None
        """
        wandb_mode = os.environ.get("WANDB_MODE", EMPTY_STRING).lower()
        if wandb_mode == "offline":
            return
        model_name = os.path.basename(model_path)
        train_name, val_name, eval_name = WBManager.get_project_names(trainer_dataset_manager)
        run_name = f"{train_name} @ {model_name}"
        if run_suffix:
            run_name = f"{run_name}({run_suffix})"
        project_name = os.environ.get("WANDB_PROJECT", eval_name)
        config = {"train_project": train_name, "val_project": val_name, "eval_project": eval_name, "model": model_path}
        wandb.init(
            project=f"{project_name}",
            name=run_name,
            config=config
        )
        cls.HAS_INITIALIZED = True

    @classmethod
    def log(cls, role2metrics: Dict[DatasetRole, Dict] = None, additional_metrics: Dict = None, step: int = None) -> None:
        """
        Logs the current metrics at given stpe prefixed with dataset role name.
        :param role2metrics: Map of role to metrics.
        :param additional_metrics: Any other metrics to append to flattened log.
        :param step: The current step to log this to.
        :return: None
        """
        if not cls.HAS_INITIALIZED:
            return
        if additional_metrics is None:
            additional_metrics = {}
        if role2metrics is None:
            role2metrics = {}
        global_metrics = {}
        for dataset_role, role_metrics in role2metrics.items():
            named_metrics = {f"{dataset_role.name.lower()}_{k}": v for k, v in role_metrics.items()}
            global_metrics.update(named_metrics)
        global_metrics.update(additional_metrics)
        wandb.log(global_metrics, step=step)

    @classmethod
    def finish(cls) -> None:
        """
        Finishes the wandb run.
        :return: None
        """
        wandb.finish()
        cls.HAS_INITIALIZED = False

    @classmethod
    def get_project_names(cls, trainer_dataset_manager: "TrainerDatasetManager") -> Tuple[Any, Any, Any]:
        """
        Calculates the name of the run identifying the training, validation, and evaluation projects.
        :param trainer_dataset_manager: The dataset manager containing the datasets whose projects names are extracted.
        :return: The run name
        """
        train_name = cls.get_project_name(trainer_dataset_manager, DatasetRole.TRAIN)
        eval_name = cls.get_project_name(trainer_dataset_manager, DatasetRole.EVAL)
        split_size = trainer_dataset_manager.get_split_size(DatasetRole.VAL)
        val_name = split_size if split_size else cls.get_project_name(trainer_dataset_manager, DatasetRole.VAL)
        return train_name, val_name, eval_name

    @staticmethod
    def get_project_name(trainer_dataset_creator: "TrainerDatasetManager", dataset_role: DatasetRole) -> str:
        """
        Gets the name of the project associated with given role.
        :param trainer_dataset_creator: Holds the creators containing the project names.
        :param dataset_role: The role of the creator whose project name is retrieved.
        :return: The name of the project at given role.
        """
        return trainer_dataset_creator.get_creator(dataset_role).get_name()
