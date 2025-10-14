from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from gen_common.data.keys.structure_keys import StructuredKeys


@dataclass
class TaskInstructions:
    """
    The instructions for extracting the task definition from a dataset's base definition.
    """
    artifacts: List[str]
    traces: List[str]
    overrides: Dict

    def as_update_iterator(self) -> Iterable[Tuple[str, List[str]]]:
        """
        :return: Returns iterator detailing how to extract task definition from base definition.
        """
        for artifact_type in self.artifacts:
            yield [StructuredKeys.ARTIFACTS, artifact_type]
        for trace_matrix in self.traces:
            yield [StructuredKeys.TRACES, trace_matrix]
