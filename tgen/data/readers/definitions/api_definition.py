from dataclasses import dataclass
from typing import List

from tgen.common.util.base_object import BaseObject
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.ranking.common.trace_layer import TraceLayer


@dataclass
class ApiDefinition(BaseObject):
    """
    Defines the dataset received through the API.
    """
    artifact_layers: dict  # Dict[str, Dict[str, str]]
    layers: List[TraceLayer]
    true_links: List[TracePredictionEntry] = None
    summary: str = None

    def get_links(self) -> List[TracePredictionEntry]:
        """
        :return: Returns the trace links defined in API dataset.
        """
        return [] if self.true_links is None else self.true_links
