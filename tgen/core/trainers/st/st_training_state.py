import json
from typing import Iterable, List, Tuple

from sentence_transformers import SentenceTransformer
from sentence_transformers.model_card_templates import ModelCardTemplate
from torch import nn
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

from tgen.core.trainers.st.constants import FIT_PARAMETERS_KEY, LOSS_FUNCTIONS_SECTION_KEY, STARTING_STEP
from tgen.core.trainers.st.st_training_params import STTrainingParams

ModelType = nn.Module
TrainingObjective = Tuple[DataLoader, ModelType]


class STTrainingState:
    def __init__(self, training_objectives: Iterable[TrainingObjective], params: STTrainingParams):
        """
        Represents state needed for training a ST model.
        :param training_objectives: The training objectives defining data and model to train.
        :param params: The training parameters.
        """
        loss_models = [loss_model for _, loss_model in training_objectives]
        dataloaders = [dataloader for dataloader, _ in training_objectives]
        self.loss_functions: List[ModelType] = loss_models
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
        for loss_model in self.loss_functions:
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
        for dataloader, loss in zip(self.data_loaders, self.loss_functions):
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
