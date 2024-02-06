from typing import List

import torch
from sentence_transformers import InputExample
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers.trainer_utils import EvalPrediction, PredictionOutput, TrainOutput

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.hugging_face_constants import DEFAULT_MAX_STEPS_BEFORE_EVAL
from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.common.logging.logger_manager import logger
from tgen.common.util.list_util import ListUtil
from tgen.common.util.override import overrides
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.st.balanced_batch_sampler import BalancedBatchSampler
from tgen.core.trainers.st.custom_sentence_transformer import CustomSentenceTransformer
from tgen.core.trainers.st.sentence_transformer_evaluator import SentenceTransformerEvaluator
from tgen.core.trainers.st.st_loss_functions import SupportedLossFunctions
from tgen.core.trainers.st.st_metrics import STMetrics
from tgen.core.trainers.st.st_training_manager import STTrainingParams
from tgen.core.trainers.st.st_utilities import calculate_similarities, to_input_examples
from tgen.core.trainers.st.tensor_utilities import move_to_device
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask


class SentenceTransformerTrainerSiamese(HuggingFaceTrainer):
    """
    Trains sentence transformer models. They have a slightly modified API for training the models and loading the data.
    """

    def __init__(self, trainer_args: HuggingFaceArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 max_steps_before_eval: int = DEFAULT_MAX_STEPS_BEFORE_EVAL, **kwargs):
        """
        Trainer for sentence transformer models. Provides API that allows training and prediction operations.
        :param trainer_args: The trainer arguments.
        :param model_manager: The model manager container sentence transformer.
        :param trainer_dataset_manager: Contains the datasets used for training, validation, and evaluation.
        :param max_steps_before_eval: The maximum number of training steps that are allowed before evaluating.
        :param loss_function: The loss function to use while training model.
        :param save_best_model: Whether to save the best model. Defaults to true
        :param kwargs: Additional keyword arguments passed to parent trainer.
        """
        model_manager.model_task = ModelTask.SBERT
        model_manager.arch_type = ModelArchitectureType.SIAMESE
        super().__init__(trainer_args, model_manager, trainer_dataset_manager, **kwargs)
        self.min_eval_steps = max_steps_before_eval
        self.losses = []
        self.total_loss = 0
        self.loss_function = None
        self.params = None  # make global step
        self.loss_function = self._create_loss_function()

    @overrides(HuggingFaceTrainer)
    def train(self, **kwargs) -> TrainOutput:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        if SupportedLossFunctions.MNRL.is_name(self.trainer_args.st_loss_function):
            self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_hf_dataset(self.model_manager, use_pos_ids=True)
            logger.info("Using only positive links in training dataset.")

        train_examples = self.to_input_examples(self.train_dataset, use_scores=self.trainer_args.use_scores, model=self.model)
        train_dataloader = DataLoader(train_examples,
                                      batch_sampler=BalancedBatchSampler(train_examples, batch_size=self.args.train_batch_size))

        n_steps = min(len(train_dataloader) + 1, self.min_eval_steps)

        evaluator = SentenceTransformerEvaluator(self, self.evaluation_roles) if self.has_dataset(DatasetRole.VAL) else None

        logger.log_title("Training...", prefix=NEW_LINE)
        model: CustomSentenceTransformer = self.model
        self.params = STTrainingParams(
            epochs=int(self.args.num_train_epochs),
            warmup_steps=self.args.warmup_steps,
            evaluation_steps=n_steps,
            evaluator=evaluator,
            output_path=self.args.output_dir,
            save_best_model=self.trainer_args.save_best_model,
            accumulation_steps=self.args.gradient_accumulation_steps
        )
        model.fit(train_objectives=[(train_dataloader, self.loss_function)], training_params=self.params)
        self.state.best_model_checkpoint = self.args.output_dir
        if self.args.load_best_model_at_end:
            self.model = CustomSentenceTransformer(self.state.best_model_checkpoint)

        metrics = STMetrics(records=evaluator.metrics, losses=self.losses)
        return TrainOutput(metrics=metrics, training_loss=self.total_loss, global_step=self.params.global_step)

    @overrides(HuggingFaceTrainer)
    def predict(self, dataset_role: DatasetRole, **kwargs) -> PredictionOutput:
        """
        Predicts on the dataset given.
        :param dataset_role: Role of dataset to predict on.
        :return: Prediction output containing similarity scores as predictions.
        """
        self._current_eval_role = dataset_role
        dataset = self._get_dataset(dataset_role)
        input_examples = to_input_examples(dataset)
        scores, labels = calculate_similarities(self.model, input_examples)
        prediction_metrics = self._compute_validation_metrics(EvalPrediction(scores, labels))
        prediction_metrics["loss"] = self.compute_internal_loss(scores, labels, input_examples)
        return PredictionOutput(scores, labels, prediction_metrics)

    def compute_internal_loss(self, scores, labels, input_examples: List[InputExample]):
        model_device = self.loss_function.model._target_device
        batches = ListUtil.batch(input_examples, self.args.train_batch_size)
        total_loss = torch.tensor(0.0, device=model_device)

        for batch in tqdm(batches, desc="Computing loss function...", ncols=TQDM_NCOLS):
            features, labels = self.model.smart_batching_collate(batch)
            features, labels = move_to_device(model_device, features, labels)
            total_loss += self.loss_function(features, labels).detach()

        return total_loss.item()

    def _create_loss_function(self):
        """
        Creates the loss function from its defined class.
        :return: The loss function.
        """
        loss_function_name = self.trainer_args.st_loss_function
        loss_function_kwargs = {}
        possible_params = {"size_average": False, "margin": 0.1}
        loss_function_class = SupportedLossFunctions.get_value(loss_function_name)
        for param, param_value in possible_params.items():
            if ReflectionUtil.has_constructor_param(loss_function_class, param):
                loss_function_kwargs[param] = param_value

        loss_function = loss_function_class(self.model, **loss_function_kwargs)
        logger.info(f"Created loss function {loss_function_name}.")
        return loss_function
