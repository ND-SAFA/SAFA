from dataclasses import dataclass, field
from typing import Callable, Dict, Type

import torch
from sentence_transformers.evaluation import SentenceEvaluator
from sentence_transformers.util import fullname
from torch.optim import Optimizer


@dataclass
class STTrainingParams:
    """
    :param evaluator: An evaluator (sentence_transformers.evaluation) evaluates the model performance during training on held-out dev data. It is used to determine the best model that is saved to disc.
    :param epochs: Number of epochs for training
    :param steps_per_epoch: Number of training steps per epoch. If set to None (default), one epoch is equal the DataLoader size from train_objectives.
    :param scheduler: Learning rate scheduler. Available schedulers: constantlr, warmupconstant, warmuplinear, warmupcosine, warmupcosinewithhardrestarts
    :param warmup_steps: Behavior depends on the scheduler. For WarmupLinear (default), the learning rate is increased from o up to the maximal learning rate. After these many training steps, the learning rate is decreased linearly back to zero.
    :param optimizer_class: Optimizer
    :param optimizer_params: Optimizer parameters
    :param weight_decay: Weight decay for model parameters
    :param evaluation_steps: If > 0, evaluate the model using evaluator after each number of training steps
    :param output_path: Storage path for the model and evaluation files
    :param save_best_model: If true, the best model (according to evaluator) is stored at output_path
    :param max_grad_norm: Used for gradient normalization.
    :param use_amp: Use Automatic Mixed Precision (AMP). Only for Pytorch >= 1.6.0
    :param callback: Callback function that is invoked after each evaluation.
            It must accept the following three parameters in this order:
            `score`, `epoch`, `steps`
    :param show_progress_bar: If True, output a tqdm progress bar
    :param checkpoint_path: Folder to save checkpoints during training
    :param checkpoint_save_steps: Will save a checkpoint after so many steps
    :param checkpoint_save_total_limit: Total number of checkpoints to stor
"""
    epochs: int
    weight_decay: float = 0.01
    optimizer_class: Type[Optimizer] = torch.optim.AdamW
    optimizer_params: Dict = field(default_factory=lambda: {"lr": 2e-5})
    scheduler_name: str = "WarmupLinear"
    warmup_steps: int = 10000
    evaluator: SentenceEvaluator = None
    evaluation_steps: int = 0
    max_grad_norm: float = 1
    use_amp: bool = False
    accumulation_steps: int = 1
    global_step: int = 0
    checkpoint_path: str = None
    checkpoint_save_steps: int = 500
    checkpoint_save_total_limit: int = 0
    output_path: str = None
    evaluation_steps: int = 0
    save_best_model: bool = True
    callback: Callable[[float, int, int], None] = None
    steps_per_epoch: int = None

    def to_model_card_params(self, steps_per_epoch: int) -> Dict:
        """
        Converts training parameters to dictionary needed for model card.
        :param steps_per_epoch:
        :return: Params as dictionary.
        """
        return {
            "evaluator": fullname(self.evaluator),
            "epochs": self.epochs,
            "steps_per_epoch": steps_per_epoch,
            "scheduler": self.scheduler_name,
            "warmup_steps": self.warmup_steps,
            "optimizer_class": str(self.optimizer_class),
            "optimizer_params": self.optimizer_params,
            "weight_decay": self.weight_decay,
            "evaluation_steps": self.evaluation_steps,
            "max_grad_norm": self.max_grad_norm,
        }

    def is_checkpoint_time(self):
        """
        :return: Whether training loop should save a checkpoint of the model.
        """
        return self.checkpoint_path is not None and self.checkpoint_save_steps is not None and self.checkpoint_save_steps > 0 and \
            self.global_step % self.checkpoint_save_steps == 0

    def can_save_best_model(self):
        """
        :return: Whether best model can be saved.
        """
        return self.evaluator is None and self.output_path is not None
