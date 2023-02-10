import json
import os
from typing import Dict, Optional

from transformers import is_torch_tpu_available
from transformers.integrations import WandbCallback

from train.trainer_args import TrainerArgs
from train.wandb.Wandb import Wandb

GROUP_EXCLUDE = ["random_seed"]


class TraceCallback(WandbCallback):
    """
    Contains modifications including setting group of run.
    """

    def setup(self, args: TrainerArgs, state, model, **kwargs) -> None:
        """
        Initialize wandb with the correct group name using experimental variables.
        :param args: The trainer args used to identify run.
        :param state: The trainer state
        :param model: The model being trained.
        :param kwargs: Any additional arguments.
        :return: None
        """
        project = os.getenv("WANDB_PROJECT", "huggingface")
        run = args.run_name
        experimental_vars = Wandb.get_clean_vars(args.experimental_vars)
        if isinstance(experimental_vars, str):
            experimental_vars = {"name": experimental_vars}
        group = self.get_group(experimental_vars)
        if self._wandb.run is None:
            self._wandb.init(
                project=project,
                name=run,
                group=group
            )
            # add config parameters (run may have been created manually)
            self._wandb.config.update(experimental_vars, allow_val_change=True)

            # define default x-axis (for latest wandb versions)
            if getattr(self._wandb, "define_metric", None):
                self._wandb.define_metric("train/global_step")
                self._wandb.define_metric("*", step_metric="train/global_step", step_sync=True)

            # keep track of model topology and gradients, unsupported on TPU
            if not is_torch_tpu_available() and os.getenv("WANDB_WATCH") != "false":
                self._wandb.watch(
                    model, log=os.getenv("WANDB_WATCH", "gradients"), log_freq=max(100, args.logging_steps)
                )

    @staticmethod
    def get_group(experimental_vars: Dict, delimiter="*") -> Optional[str]:
        """
        Returns the name of the group using priority of group properties.
        :param experimental_vars: The experimental variables to find group for.
        :param delimiter: The delimiter used to combine groups into identifier.
        :return: Returns the first group property contained in experimental vars, None otherwise.
        """
        group = []
        for k, v in experimental_vars.items():
            if k in GROUP_EXCLUDE:
                continue
            group.append(json.dumps({TraceCallback.get_group_id(k): v}))
        return None if len(group) == 0 else delimiter.join(group)  # no grouping if none exists, else return group

    @staticmethod
    def get_group_id(group_name: str):
        """
        :param group_name: The name whose id is returned.
        :return: Returns the initials of group name.
        """
        if "_" in group_name:
            group_parts = group_name.split("_")
            group_parts = [g[0] for g in group_parts]
        else:
            group_parts = [group_name[0]]
        return "".join(group_parts)
