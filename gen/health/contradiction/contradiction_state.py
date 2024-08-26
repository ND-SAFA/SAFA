from dataclasses import field
from typing import List

from gen_common.pipeline.state import State

from gen.health.contradiction.contradiction_result import ContradictionResult


class ContradictionState(State):
    """
    List of contradictions found in query artifacts.
    """
    contradictions: List[ContradictionResult] = field(default_factory=lambda: [])
