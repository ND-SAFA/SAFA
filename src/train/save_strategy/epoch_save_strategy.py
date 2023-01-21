from typing import Dict

from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy, ComparisonFunction, SaveStrategyStage


class MetricSaveStrategy(AbstractSaveStrategy):
    """
    Defines save strategy that occurs at the end of each n epochs
    """

    def __init__(self, stage: SaveStrategyStage = SaveStrategyStage.EPOCH, interval=1, metric_name: str = None,
                 comparison: ComparisonFunction = ComparisonFunction.MAX):
        super().__init__()
        self.stage = stage
        self.interval = interval
        self.metric_name = metric_name
        self.comparison = comparison
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

    def should_save(self, evaluation_result: Dict) -> bool:
        """
        Returns whether current evaluation is the best one yet.
        :param evaluation_result: The result of evaluating the model.
        :return: If evaluation is best.
        """
        super().should_save(evaluation_result)
        score = evaluation_result[self.metric_name]
        return self.comparison.value(score, self.best_score)
