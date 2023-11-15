import json
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple, Type

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import SentenceEvaluator
from sentence_transformers.model_card_templates import ModelCardTemplate
from sentence_transformers.util import batch_to_device, fullname
from torch import nn
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

ModelType = nn.Module
TrainingObjective = Tuple[DataLoader, ModelType]


@dataclass
class TrainingDataParams:
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

    def to_dict(self, steps_per_epoch: int) -> Dict:
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
        return self.checkpoint_path is not None and self.checkpoint_save_steps is not None and self.checkpoint_save_steps > 0 and \
            self.global_step % self.checkpoint_save_steps == 0

    def should_save_final_model(self):
        return self.evaluator is None and self.output_path is not None


class TrainingData:
    def __init__(self, training_objectives: Iterable[TrainingObjective], params: TrainingDataParams):
        loss_models = [loss_model for _, loss_model in training_objectives]
        dataloaders = [dataloader for dataloader, _ in training_objectives]
        self.models: List[ModelType] = loss_models
        self.data_loaders: List[DataLoader] = dataloaders
        self.data_iterators = None
        self.params = params
        self.optimizers, self.schedulers = self.initialize_optimizers_schedulers()

    def initialize_optimizers_schedulers(self) -> Tuple[List[Optimizer], List[_LRScheduler]]:
        optimizers = []
        schedulers = []
        for loss_model in self.models:
            param_optimizer = list(loss_model.named_parameters())

            no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
            optimizer_grouped_parameters = [
                {
                    "params": [
                        p for n, p in param_optimizer if not any(nd in n for nd in no_decay)
                    ],
                    "weight_decay": self.params.weight_decay,
                },
                {
                    "params": [
                        p for n, p in param_optimizer if any(nd in n for nd in no_decay)
                    ],
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
        info_loss_functions = []
        for dataloader, loss in zip(self.data_loaders, self.models):
            info_loss_functions.extend(
                ModelCardTemplate.get_train_objective_info(dataloader, loss)
            )
        info_loss_functions = "\n\n".join([text for text in info_loss_functions])

        params_dict = self.params.to_dict(self.get_epoch_steps())
        info_fit_parameters = json.dumps(params_dict, indent=4, sort_keys=True)
        return ModelCardTemplate.__TRAINING_SECTION__.replace(
            "{LOSS_FUNCTIONS}", info_loss_functions
        ).replace(
            "{FIT_PARAMETERS}", info_fit_parameters
        )

    def perform_training_step(self, training_step: int, target_device: str):
        if self.data_iterators is None:
            self.initialize_data_iterators()

        for train_idx in range(len(self.models)):
            loss_model = self.models[train_idx]
            optimizer = self.optimizers[train_idx]
            scheduler = self.schedulers[train_idx]
            data_iterator = self.data_iterators[train_idx]

            data = next(data_iterator)

            features, labels = data
            labels = labels.to(target_device)
            features = list(map(lambda batch: batch_to_device(batch, target_device), features))

            loss_value = loss_model(features, labels)
            loss_value /= self.params.accumulation_steps
            loss_value.backward()

            if training_step % self.params.accumulation_steps == 0:
                torch.nn.utils.clip_grad_norm_(loss_model.parameters(), self.params.max_grad_norm)
                optimizer.step()
                optimizer.zero_grad()

            scheduler.step()

        self.params.global_step += 1

    def initialize_data_iterators(self):
        self.data_iterators = [iter(dl) for dl in self.data_loaders]

    def get_epoch_steps(self) -> int:
        steps_per_epoch = min([len(dataloader) for dataloader in self.data_loaders])
        return steps_per_epoch

    def get_total_steps(self):
        n_epoch_steps = self.get_epoch_steps()
        return n_epoch_steps * self.params.epochs
