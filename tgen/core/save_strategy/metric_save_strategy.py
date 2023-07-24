from typing import Dict

from tgen.core.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from tgen.core.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.core.save_strategy.save_strategy_stage import SaveStrategyStage
from tgen.core.trace_output.stage_eval import Metrics


class MetricSaveStrategy(AbstractSaveStrategy):
    """
    Defines save strategy that defines the best metrics using a prioritized list of metrics.
    """

    def __init__(self, comparison_criterion: ComparisonCriterion, stage: SaveStrategyStage = SaveStrategyStage.EPOCH,
                 interval: int = 1, delta: int = 0.001):
        """
        Creates save strategy evaluating at the given stage at the interval defined.
        :param comparison_criterion: How to compare metrics to determine the best one.
        :param stage: Whether the interval is every n epochs or steps.
        :param interval: How many iterations of the stage to evaluate at.
        :param delta: How close the metrics that are the "same" should be.
        """
        super().__init__()
        self.stage = stage
        self.interval = interval
        self.comparison_criterion = comparison_criterion
        self.comparison_metrics = comparison_criterion.metrics
        self.comparison_function = comparison_criterion.comparison_function
        self.iteration = 0
        self.best_scores = None
        self.best_iteration = None
        self.delta = delta

    def should_evaluate(self, stage: SaveStrategyStage, stage_iteration: int) -> bool:
        """
        Returns true is stage iteration is multiple of defined interval.
        :param stage: The stage of the training loop.
        :param stage_iteration: The number of times stage has been performed.
        :return: Whether model should be evaluated.
        """
        return stage == self.stage and self.iteration % self.interval == 0

    def should_save(self, metrics: Metrics, evaluation_id: int) -> bool:
        """
        Returns whether current evaluation is the best one yet.
        :param metrics: The result of evaluating the model.
        :param evaluation_id: The id of the evaluation.
        :return: True if evaluation is best and false otherwise.
        """
        super().should_save(metrics, evaluation_id)
        if self.best_scores is None or self._is_better(metrics):
            self.store_best(metrics)
            return True
        return False

    def _is_better(self, metrics: Metrics) -> bool:
        """
        Returns if metrics is better than current metrics.
        Calculates best in each metric and using other metrics to decide tie-breakers.
        :param metrics: The metrics to compare against the current best.
        :return: Whether given metrics is better than current.
        """
        for metric_name in self.comparison_criterion.metrics:
            self_score = self.best_scores[metric_name]
            other_score = metrics[metric_name]
            if abs(self_score - other_score) <= self.delta:
                continue
            return self.comparison_function(other_score, self_score)

    def store_best(self, metrics: Metrics) -> None:
        """
        Stores evaluation as the new best.
        :param metrics: The evaluation result stored as current best.
        :return: None
        """
        self.best_scores = {m: v for m, v in metrics.items()}

    def get_metric_scores(self, evaluation_metrics: Metrics) -> Dict:
        """
        Returns the score of the evaluation metric in given metrics.
        :param evaluation_metrics: The metrics to extract the score from.
        :return: The metric score.
        """
        return {m: evaluation_metrics[m] for m in self.comparison_criterion.metrics}
