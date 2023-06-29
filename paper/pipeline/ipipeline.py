from typing import Callable, List

from paper.pipeline.base import RankingStore


class iPipeline:
    def __init__(self, steps: List[Callable[[RankingStore], None]]):
        self.steps = steps

    def __call__(self, s: RankingStore):
        for step in self.steps:
            step(s)
