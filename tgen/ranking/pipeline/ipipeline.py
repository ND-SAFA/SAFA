from typing import Callable, List

from tgen.ranking.pipeline.base import RankingStore


class iPipeline:

    def __init__(self, steps: List[Callable[[RankingStore], None]]):
        """
        Constructs pipeline of steps.
        :param steps: Steps to perform in sequential order.
        """
        self.steps = steps

    def __call__(self, s: RankingStore) -> None:
        """
        Runs steps with store.
        :param s: The ranking store.
        :return: None
        """
        for step in self.steps:
            step(s)
