from typing import Type

from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.state import State

from gen.health.contradiction.contradiction_state import ContradictionState
from gen.health.contradiction.steps.detect_contradiction_step import DetectContradictionStep
from gen.health.health_args import HealthArgs


class ContradictionPipeline(AbstractPipeline[HealthArgs, ContradictionState]):
    steps = [DetectContradictionStep]

    def __init__(self, args: HealthArgs):
        """
        Creates contradictions pipeline for given health args.
        :param args: Arguments defining artifacts and query artifacts.
        """
        super().__init__(args, self.steps)

    def state_class(self) -> Type[State]:
        """
        :return: Returns Health state class
        """
        return ContradictionState
