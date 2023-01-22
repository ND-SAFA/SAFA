from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from train.save_strategy.comparison_criteria import ComparisonCriterion
from train.save_strategy.save_strategy_stage import SaveStrategyStage
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
        self.stage = stage
        self.interval = interval
        self.comparison_criterion = comparison_criterion
        self.iteration = 0
        self.best_score = None
        self.best_iteration = None
        assert len(self.comparison_criterion.metrics) == 1, "Expected single criterion metric."

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
        score = evaluation_result.metrics[self.metric_name]
        return self.comparison.value(score, self.best_score)
