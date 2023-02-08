import os
from typing import Dict, Optional

from transformers import is_torch_tpu_available
from transformers.integrations import WandbCallback

from train.trainer_args import TrainerArgs

GROUP_PROPERTIES = ["project_path"]


class TraceCallback(WandbCallback):
    """
    Contains modifications including setting group of run.
    """

    def setup(self, args: TrainerArgs, state, model, **kwargs):
        project = os.getenv("WANDB_PROJECT", "huggingface")
        run = args.run_name
        group = self.get_group(args.experimental_vars)
        if self._wandb.run is None:
            self._wandb.init(
                project=project,
                name=run,
                group=group
            )
            # add config parameters (run may have been created manually)
            self._wandb.config.update(args.experimental_vars, allow_val_change=True)

            # define default x-axis (for latest wandb versions)
            if getattr(self._wandb, "define_metric", None):
                self._wandb.define_metric("train/global_step")
                self._wandb.define_metric("*", step_metric="train/global_step", step_sync=True)

            # keep track of model topology and gradients, unsupported on TPU
            if not is_torch_tpu_available() and os.getenv("WANDB_WATCH") != "false":
                self._wandb.watch(
                    model, log=os.getenv("WANDB_WATCH", "gradients"), log_freq=max(100, args.logging_steps)
                )

    def get_group(self, experimental_vars: Dict) -> Optional[str]:
        """
        Returns the name of the group using priority of group properties.
        :param experimental_vars:
        :return:
        """
        for prop in GROUP_PROPERTIES:
            if prop in experimental_vars:
                return experimental_vars[prop]
        return None
