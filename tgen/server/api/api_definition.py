from dataclasses import dataclass
from typing import List

from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.ranking.common.trace_layer import TraceLayer
from tgen.util.base_object import BaseObject


@dataclass
class ApiDefinition(BaseObject):
    """
    Defines the dataset received through the API.
    """
    artifact_layers: dict  # maps layer names to layer artifact maps.
    layers: List[TraceLayer]
    true_links: List[TracePredictionEntry] = None

    def get_links(self) -> List[TracePredictionEntry]:
        """
        :return: Returns the trace links defined in API dataset.
        """
        return [] if self.true_links is None else self.true_links
