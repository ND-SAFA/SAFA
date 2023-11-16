import json
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Tuple, Type

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import SentenceEvaluator
from sentence_transformers.model_card_templates import ModelCardTemplate
from sentence_transformers.util import fullname
from torch import nn
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

from tgen.core.trainers.st.constants import FIT_PARAMETERS_KEY, LOSS_FUNCTIONS_SECTION_KEY, STARTING_STEP

ModelType = nn.Module
TrainingObjective = Tuple[DataLoader, ModelType]


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


class STTrainingManager:
    def __init__(self, training_objectives: Iterable[TrainingObjective], params: STTrainingParams):
        """
        Constructs training manager with given objectives and parameteres.
        :param training_objectives: The training objectives defining data and model to train.
        :param params: The training parameters.
        """
        loss_models = [loss_model for _, loss_model in training_objectives]
        dataloaders = [dataloader for dataloader, _ in training_objectives]
        self.models: List[ModelType] = loss_models
        self.data_loaders: List[DataLoader] = dataloaders
        self.data_iterators = None
        self.params = params
        self.optimizers, self.schedulers = self.initialize_optimizers_schedulers()

    def initialize_optimizers_schedulers(self) -> Tuple[List[Optimizer], List[_LRScheduler]]:
        """
        Creates the optimizers and schedulers for this training session.
        :return:
        """
        optimizers = []
        schedulers = []
        for loss_model in self.models:
            param_optimizer = list(loss_model.named_parameters())

            no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
            optimizer_grouped_parameters = [
                {
                    "params": [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
                    "weight_decay": self.params.weight_decay,
                },
                {
                    "params": [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
                    "weight_decay": 0.0,
                },
            ]

            optimizer = self.params.optimizer_class(optimizer_grouped_parameters, **self.params.optimizer_params)
            scheduler_obj = SentenceTransformer._get_scheduler(
                optimizer,
                scheduler=self.params.scheduler_name,
                warmup_steps=self.params.warmup_steps,
                t_total=self.get_total_steps(),
            )

            optimizers.append(optimizer)
            schedulers.append(scheduler_obj)
        return optimizers, schedulers

    def get_model_card_training_info(self):
        """
        Creates the model card information containing the training configuration.
        :return: String representing the model card information.
        """
        info_loss_functions = []
        for dataloader, loss in zip(self.data_loaders, self.models):
            info_loss_functions.extend(
                ModelCardTemplate.get_train_objective_info(dataloader, loss)
            )
        info_loss_functions = "\n\n".join([text for text in info_loss_functions])

        params_dict = self.params.to_model_card_params(self.get_epoch_steps())
        info_fit_parameters = json.dumps(params_dict, indent=4, sort_keys=True)
        return ModelCardTemplate \
            .__TRAINING_SECTION__ \
            .replace(LOSS_FUNCTIONS_SECTION_KEY, info_loss_functions) \
            .replace(FIT_PARAMETERS_KEY, info_fit_parameters)

    def get_training_iterator(self) -> List[Tuple[int, int]]:
        """
        Returns the list of epoch and training step tuples for entire training loop.
        :return: List of tuples containing epoch and training step.
        """
        steps_per_epoch = self.get_epoch_steps()
        training_iterations = [(epoch + STARTING_STEP, step + STARTING_STEP)
                               for epoch in range(self.params.epochs) for step in range(steps_per_epoch)]
        return training_iterations

    def initialize_data_iterators(self) -> None:
        """
        Constructs an iterator for each data loader.
        :return: None.
        """
        self.data_iterators = [iter(dl) for dl in self.data_loaders]

    def get_epoch_steps(self) -> int:
        """
        :return: Returns the number of training steps per epoch.
        """
        if self.params.steps_per_epoch:
            return self.params.steps_per_epoch
        steps_per_epoch = min([len(dataloader) for dataloader in self.data_loaders])
        return steps_per_epoch

    def get_total_steps(self):
        """
        :return: Returns the total number of training steps in the training loop configuration.
        """
        n_epoch_steps = self.get_epoch_steps()
        return n_epoch_steps * self.params.epochs
