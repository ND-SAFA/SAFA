import os

from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from transformers import is_torch_tpu_available
from transformers.integrations import WandbCallback


class TraceCallback(WandbCallback):
    """
    Contains modifications including setting group of run.
    """

    def setup(self, args: HuggingFaceArgs, state, model, **kwargs) -> None:
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
        if self._wandb.run is None:
            self._wandb.init(
                project=project,
                name=run
            )
            # define default x-axis (for latest wandb versions)
            if getattr(self._wandb, "define_metric", None):
                self._wandb.define_metric("train/global_step")
                self._wandb.define_metric("*", step_metric="train/global_step", step_sync=True)

            # keep track of model topology and gradients, unsupported on TPU
            if not is_torch_tpu_available() and os.getenv("WANDB_WATCH") != "false":
                self._wandb.watch(
                    model, log=os.getenv("WANDB_WATCH", "gradients"), log_freq=max(100, args.logging_steps)
                )
