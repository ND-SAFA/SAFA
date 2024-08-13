from typing import List

from sentence_transformers.evaluation import SentenceEvaluator

from common_resources.tools.constants.hugging_face_constants import SEPARATOR_BAR
from common_resources.tools.t_logging.logger_manager import logger
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.wb.wb_manager import WBManager
from common_resources.data.tdatasets.dataset_role import DatasetRole


class STEvaluator(SentenceEvaluator):
    def __init__(self, trainer: HuggingFaceTrainer, evaluation_roles: List[DatasetRole], evaluator_metric: str):
        """
        Evaluates dataset under role with given trainer.
        :param trainer: The trainer used to predict on the dataset.
        :param evaluation_roles: The role the dataset to predict should be found under.
        :param evaluator_metric: The metric used to define which is the best run.
        """
        self.trainer = trainer
        self.evaluation_roles = evaluation_roles
        self.evaluator_metric = evaluator_metric
        self.metrics = []

    def __call__(self, *args, **kwargs) -> float:
        """
        Evaluates the model on the evaluation dataset.
        :param model: The model to evaluate.
        :param kwargs: Ignored.
        :return: The score for this evaluation run.
        """
        validation_metrics = None
        role2metrics = {}
        for eval_role in self.evaluation_roles:
            if not self.trainer.has_dataset(eval_role):
                logger.warning(f"Skipping evaluation on {eval_role} dataset. Defined in evaluation roles but empty.")
                continue
            prediction_output: TracePredictionOutput = self.trainer.perform_prediction(eval_role)
            logger.info(SEPARATOR_BAR)
            metrics = prediction_output.metrics
            if eval_role == DatasetRole.VAL:
                validation_metrics = metrics
            role2metrics[eval_role] = metrics

        self.metrics.append(role2metrics)
        WBManager.log(role2metrics, step=self.trainer.state.global_step)
        return validation_metrics[self.evaluator_metric]
