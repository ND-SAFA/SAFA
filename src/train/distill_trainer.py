import math
import os
from typing import Tuple, Any, Dict

import numpy as np
import torch
from torch.nn.modules.loss import MSELoss, CrossEntropyLoss
from torch.utils.data.dataloader import DataLoader
from tqdm import trange
from transformers.file_utils import WEIGHTS_NAME, CONFIG_NAME
from transformers.modeling_utils import PreTrainedModel
from transformers.trainer_utils import PredictionOutput, SchedulerType, TrainOutput

from data.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.logging.logger_manager import logger
from util.override import overrides

ModelOutputType = Tuple[Any, Any, Any]


class State:
    tr_loss, tr_att_loss, tr_rep_loss, tr_cls_loss = range(4)

    def __init__(self, global_step: int = 0):
        """
        Represents the current training state
        :param global_step: The total number of steps across all epochs
        """
        self.losses = [0., 0., 0., 0.]
        self.global_step = global_step
        self.nb_tr_examples, self.nb_tr_steps = 0, 0


class DistillTrainer(TraceTrainer):
    # These should be moved eventually to trainer args or constants
    OUTPUT_MODE = "classification"
    DISTILL_PRED_LAYER_ONLY = True
    TEMPERATURE = 1

    def __init__(self, trainer_args: TrainerArgs, student_model_manager: ModelManager, teacher_model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, save_strategy: AbstractSaveStrategy = None, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param trainer_args: The learning model arguments
        :param student_model_manager: The manager for the model used for training and/or predicting
        :param trainer_dataset_manager: The manager for the datasets used for training and/or predicting
        :param save_strategy: The strategy used to save the best model
        :param kwargs: Any additional arguments given to the HF Trainer
        """
        super().__init__(trainer_args=trainer_args, model_manager=student_model_manager,
                         trainer_dataset_manager=trainer_dataset_manager, save_strategy=save_strategy)
        self.teacher_model_manager = teacher_model_manager

    @overrides(TraceTrainer)
    def _inner_training_loop(self, batch_size=None, **kwargs) -> TrainOutput:
        """
        Overrides the training loop in Trace Trainer to perform distillation training
        :param batch_size: The size of the batch
        :param kwargs: Any other arguments given by the base trainer
        :return: The output from the training
        """
        student_model, teacher_model = self._prepare_models()

        self._train_batch_size = batch_size
        train_dataloader, max_steps, num_train_epochs = self._prepare_data()

        self.args.lr_scheduler_type = SchedulerType.LINEAR if self.DISTILL_PRED_LAYER_ONLY else SchedulerType.CONSTANT
        self.create_optimizer_and_scheduler(num_training_steps=max_steps)

        output_eval_file = os.path.join(self.args.output_dir, "eval_results.txt")
        best_result = 0
        total_loss = 0
        global_step = 0
        result = {}
        for epoch in trange(num_train_epochs, desc="Epoch"):
            state = State(global_step)
            student_model.train()

            for step, inputs in enumerate(train_dataloader):
                state = self._training_step(inputs, student_model, teacher_model, state)
                if (step + 1) % self.args.gradient_accumulation_steps == 0:
                    self.optimizer.step()
                    self.optimizer.zero_grad()
                    global_step += 1
                if (global_step + 1) % self.args.eval_steps == 0 and self.eval_dataset:
                    result = self._do_step_eval(epoch, step, output_eval_file, student_model, state, best_result)
            total_loss += state.losses[state.tr_loss]
        return TrainOutput(global_step, total_loss, result)

    def _training_step(self, inputs: torch.Tensor, student_model: PreTrainedModel, teacher_model: PreTrainedModel, state: State) \
            -> State:
        """
        Performs a single training step
        :param inputs: The inputs for the batch
        :param student_model: The student model
        :param teacher_model: The teacher model
        :param state: Current state
        :return: Updated state
        """
        inputs = self._prepare_inputs(inputs)
        labels = inputs.pop("labels")
        att_loss, rep_loss = 0., 0.
        student_output = student_model(**inputs, is_student=True)
        with torch.no_grad():
            teacher_output = teacher_model(**inputs)
        if self.DISTILL_PRED_LAYER_ONLY:
            cls_loss = self._compute_distill_loss_pred_layer_only(student_output, teacher_output, self.TEMPERATURE, labels)
            loss = cls_loss
            state.losses[State.tr_cls_loss] += cls_loss.item()

        else:
            att_loss, rep_loss = self._compute_distill_loss_all_layers(student_output, teacher_output, att_loss, rep_loss)

            loss = rep_loss + att_loss
            state.losses[State.tr_att_loss] += att_loss.item()
            state.losses[State.tr_rep_loss] += rep_loss.item()
        if self.args.n_gpu > 1:
            loss = loss.mean()  # mean() to average on multi-gpu.
        if self.args.gradient_accumulation_steps > 1:
            loss = loss / self.args.gradient_accumulation_steps
        loss.backward()
        state.losses[State.tr_loss] += loss.item()
        state.nb_tr_examples += labels.size(0)
        state.nb_tr_steps += 1
        return state

    def _do_step_eval(self, epoch: int, step: int, output_eval_file: str, student_model: PreTrainedModel, state: State,
                      best_result: float) -> Dict[str, float]:
        """
        Performs the evaluation for the step
        :param epoch: Current epoch number
        :param step: Current step number for epoch
        :param output_eval_file: The path to the file to save the results
        :param student_model: The student model
        :param state: The current training state
        :param best_result: The current best result
        :return: The results from the step
        """
        logger.info("***** Running evaluation *****")
        logger.info("  Epoch = {} iter {} step".format(epoch, state.global_step))
        logger.info("  Num examples = %d", len(self.eval_dataset))
        logger.info("  Batch size = %d", self.args.eval_batch_size)
        student_model.eval()
        loss = state.losses[state.tr_loss] / (step + 1)
        cls_loss = state.losses[state.tr_cls_loss] / (step + 1)
        att_loss = state.losses[state.tr_att_loss] / (step + 1)
        rep_loss = state.losses[state.tr_rep_loss] / (step + 1)
        result = self._get_result(state.global_step, cls_loss, att_loss, rep_loss, loss)
        if self.DISTILL_PRED_LAYER_ONLY:
            result = {**result, **self._do_eval(student_model)}
        self._result_to_file(result, output_eval_file)
        save_model = not self.DISTILL_PRED_LAYER_ONLY or self._should_save(result, best_result)
        if save_model:
            self._model_save(student_model)
        student_model.train()
        return result

    def _model_save(self, model: PreTrainedModel) -> None:
        """
        Saves the model and necessary state
        :param model: The model to save
        :return: None
        """
        logger.info("***** Save model *****")
        model_to_save = model.module if hasattr(model, 'module') else model
        model_name = WEIGHTS_NAME
        output_model_file = os.path.join(self.args.output_dir, model_name)
        output_config_file = os.path.join(self.args.output_dir, CONFIG_NAME)
        torch.save(model_to_save.state_dict(), output_model_file)
        model_to_save.config.to_json_file(output_config_file)
        self.tokenizer.save_vocabulary(self.args.output_dir)

    def _prepare_models(self) -> Tuple[PreTrainedModel, PreTrainedModel]:
        """
        Prepares the student and teacher models for training
        :return: The student and teacher models
        """
        student_model = self._wrap_model(self.model_wrapped)
        teacher_model = self.teacher_model_manager.get_model()
        self._move_model_to_device(teacher_model, self.args.device)
        teacher_model = self._wrap_model(teacher_model)
        self.model = student_model
        return student_model, teacher_model

    def _compute_distill_loss_pred_layer_only(self, student_output: ModelOutputType, teacher_output: ModelOutputType,
                                              temperature: float, label_ids: torch.Tensor) -> torch.Tensor:
        """
        Computes the distillation loss for the prediction layer only
        :param student_output: The output from the student model
        :param teacher_output: The output from the teacher model
        :param temperature: Temperature constant for entropy
        :param label_ids: Contains the ground truth labels
        :return: The current cls_loss
        """
        student_logits, student_atts, student_reps = student_output
        teacher_logits, teacher_atts, teacher_reps = teacher_output

        if self.OUTPUT_MODE == "classification":
            cls_loss = self._soft_cross_entropy(student_logits / temperature,
                                                teacher_logits / temperature)
        elif self.OUTPUT_MODE == "regression":
            loss_mse = MSELoss()
            cls_loss = loss_mse(student_logits.view(-1), label_ids.view(-1))
        else:
            raise Exception("Unknown output mode %s" % self.OUTPUT_MODE)
        return cls_loss

    def _compute_distill_loss_all_layers(self, student_output: ModelOutputType, teacher_output: ModelOutputType,
                                         att_loss: float, rep_loss: float) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes the distillation loss for all layers
        :param student_output: The output from the student model
        :param teacher_output: The output from the teacher model
        :param att_loss: Previous accumulated loss from attention layers
        :param rep_loss: Previous accumulated loss from all encoding layers
        :return: The current total att_loss and rep_loss
        """
        student_logits, student_atts, student_reps = student_output
        teacher_logits, teacher_atts, teacher_reps = teacher_output
        loss_mse = MSELoss()
        teacher_layer_num = len(teacher_atts)
        student_layer_num = len(student_atts)
        assert teacher_layer_num % student_layer_num == 0
        layers_per_block = int(teacher_layer_num / student_layer_num)
        new_teacher_atts = [teacher_atts[i * layers_per_block + layers_per_block - 1]
                            for i in range(student_layer_num)]

        for student_att, teacher_att in zip(student_atts, new_teacher_atts):
            student_att = torch.where(student_att <= -1e2, torch.zeros_like(student_att).to(self.args.device),
                                      student_att)
            teacher_att = torch.where(teacher_att <= -1e2, torch.zeros_like(teacher_att).to(self.args.device),
                                      teacher_att)

            tmp_loss = loss_mse(student_att, teacher_att)
            att_loss += tmp_loss

        new_teacher_reps = [teacher_reps[i * layers_per_block] for i in range(student_layer_num + 1)]
        new_student_reps = student_reps
        for student_rep, teacher_rep in zip(new_student_reps, new_teacher_reps):
            tmp_loss = loss_mse(student_rep, teacher_rep)
            rep_loss += tmp_loss

        return att_loss, rep_loss

    @staticmethod
    def _soft_cross_entropy(predicts: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Computes the cross entropy using "soft" labels from the teacher model
        :param predicts: The predicted labels
        :param targets: The target predictions
        :return: The cross entropy loss
        """
        student_likelihood = torch.nn.functional.log_softmax(predicts, dim=-1)
        targets_prob = torch.nn.functional.softmax(targets, dim=-1)
        return (- targets_prob * student_likelihood).mean()

    def _do_eval(self, model: PreTrainedModel) -> Dict[str, float]:
        """
        Performs an evaluation of the model's predictions
        :param model: The model to evaluation
        :return: The evaluation results
        """
        eval_dataloader = self.get_eval_dataloader()
        num_labels = 2
        eval_loss = 0
        nb_eval_steps = 0
        preds = []

        for step, inputs in enumerate(eval_dataloader):
            inputs = self._prepare_inputs(inputs)
            labels = inputs.pop("labels")
            with torch.no_grad():
                logits, _, _ = model(**inputs)

            # create eval loss and other metric required by the task
            if self.OUTPUT_MODE == "classification":
                loss_fct = CrossEntropyLoss()
                tmp_eval_loss = loss_fct(logits.view(-1, num_labels), labels.view(-1))
            elif self.OUTPUT_MODE == "regression":
                loss_fct = MSELoss()
                tmp_eval_loss = loss_fct(logits.view(-1), labels.view(-1))
            else:
                raise Exception("Unknown output mode")

            eval_loss += tmp_eval_loss.mean().item()
            nb_eval_steps += 1
            if len(preds) == 0:
                preds.append(logits.detach().cpu().numpy())
            else:
                preds[0] = np.append(
                    preds[0], logits.detach().cpu().numpy(), axis=0)

        eval_loss = eval_loss / nb_eval_steps

        preds = preds[0]
        output = PredictionOutput(predictions=preds, label_ids=None, metrics={})
        result = self._compute_validation_metrics(output)
        result['eval_loss'] = eval_loss

        return result

    def _prepare_data(self) -> Tuple[DataLoader, int, int]:
        """
        Gets the train dataloader and calculates the correct size of the data
        :return: The train dataloader, the max number of steps for each epoch, and the number of training epochs
        """
        total_train_batch_size = self.args.train_batch_size * self.args.gradient_accumulation_steps * self.args.world_size
        train_dataloader = self.get_train_dataloader()
        len_dataloader = len(train_dataloader)
        num_update_steps_per_epoch = len_dataloader // self.args.gradient_accumulation_steps
        num_update_steps_per_epoch = max(num_update_steps_per_epoch, 1)
        num_examples = self.num_examples(train_dataloader)
        if self.args.max_steps > 0:
            max_steps = self.args.max_steps
            num_train_epochs = self.args.max_steps // num_update_steps_per_epoch + int(
                self.args.max_steps % num_update_steps_per_epoch > 0
            )
        else:
            max_steps = math.ceil(self.args.num_train_epochs * num_update_steps_per_epoch)
            num_train_epochs = math.ceil(self.args.num_train_epochs)
        self._log_data(self.args, num_examples, num_train_epochs, total_train_batch_size, max_steps)
        return train_dataloader, max_steps, num_train_epochs

    @staticmethod
    def _log_data(args: TrainerArgs, num_examples: int, num_train_epochs: int, total_train_batch_size: int, max_steps: int) -> None:
        """
        Logs information about the data
        :param args: The trainer args
        :param num_examples: The size of the data
        :param num_train_epochs: The number of training epochs
        :param total_train_batch_size: The total batch size for training
        :param max_steps: The max number of steps per epoch
        :return: None
        """
        logger.info("***** Running training *****")
        logger.info(f"  Num examples = {num_examples}")
        logger.info(f"  Num Epochs = {num_train_epochs}")
        logger.info(f"  Instantaneous batch size per device = {args.per_device_train_batch_size}")
        logger.info(f"  Total train batch size (w. parallel, distributed & accumulation) = {total_train_batch_size}")
        logger.info(f"  Gradient Accumulation steps = {args.gradient_accumulation_steps}")
        logger.info(f"  Total optimization steps = {max_steps}")

    def _should_save(self, result: Dict[str, float], current_best_result: float):
        """
        Returns True if the model should be saved, else False
        :param result: The results from the last epoch
        :param current_best_result: The current best result
        :return: True if the model should be saved else False
        """
        return self.trainer_args.metric_for_best_model in result and result[
            self.trainer_args.metric_for_best_model] > current_best_result

    @staticmethod
    def _get_result(global_step: int, cls_loss: float, att_loss: float, rep_loss: float, loss: float) -> Dict[str, float]:
        """
        Creates a dictionary of the current results
        :param global_step: The total step count across all epochs
        :param cls_loss: The total class loss
        :param att_loss: The total loss across attention layers
        :param rep_loss: The total loss across all encoding layers
        :param loss: The total loss
        :return: A dictionary mapping result name to the value
        """
        result = {'global_step': global_step, 'cls_loss': cls_loss, 'att_loss': att_loss, 'rep_loss': rep_loss, 'loss': loss}
        return result

    @staticmethod
    def _result_to_file(result: Dict[str, int], file_name: str) -> None:
        """
        Saves the results to a file
        :param result: The results
        :param file_name: The name of the file to save the results
        :return: None
        """
        with open(file_name, "a") as writer:
            logger.info("***** Eval results *****")
            for key in sorted(result.keys()):
                logger.info("  %s = %s", key, str(result[key]))
                writer.write("%s = %s\n" % (key, str(result[key])))
