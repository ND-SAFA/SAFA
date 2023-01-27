from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from train.save_strategy.comparison_criteria import ComparisonCriterion
from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.stage_eval import Metrics
from train.trace_output.trace_prediction_output import TracePredictionOutput


class MetricSaveStrategy(AbstractSaveStrategy):
    """
    Defines save strategy that occurs at the end of each n epochs
    """

    def __init__(self, comparison_criterion: ComparisonCriterion, stage: SaveStrategyStage = SaveStrategyStage.EPOCH,
                 interval: int = 1):
        """
        Creates save strategy evaluating at the given stage at the interval defined.
        :param comparison_criterion: How to compare metrics to determine the best one.
        :param stage: Whether the interval is every n epochs or steps.
        :param interval: How many iterations of the stage to evaluate at.
        """
        super().__init__()
        assert len(comparison_criterion.metrics) == 1, "Expected single criterion metric."
        self.stage = stage
        self.interval = interval
        self.comparison_criterion = comparison_criterion
        self.comparison_metric = comparison_criterion.metrics[0]
        self.comparison_function = comparison_criterion.comparison_function
        self.iteration = 0
        self.best_score = None
        self.best_iteration = None

    def should_evaluate(self, stage: SaveStrategyStage, stage_iteration: int) -> bool:
        """
        Returns true is stage iteration is multiple of defined interval.
        :param stage: The stage of the training loop.
        :param stage_iteration: The number of times stage has been performed.
        :return: Whether model should be evaluated.
        """
        return stage == self.stage and self.iteration % self.interval == 0

    def should_save(self, evaluation_result: TracePredictionOutput) -> bool:
        """
        Returns whether current evaluation is the best one yet.
        :param evaluation_result: The result of evaluating the model.
        :return: True if evaluation is best and false otherwise.
        """
        super().should_save(evaluation_result)
        score = evaluation_result.metrics[self.comparison_metric]
        return self.comparison_function(score, self.best_score)

    def get_metric_score(self, evaluation_metrics: Metrics) -> float:
        """
        Returns the score of the evaluation metric in given metrics.
        :param evaluation_metrics: The metrics to extract the score from.
        :return: The metric score.
        """
        return evaluation_metrics[self.comparison_metric]
