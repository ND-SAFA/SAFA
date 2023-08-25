from dataclasses import dataclass
from typing import List

from tgen.common.artifact import Artifact
from tgen.common.util.base_object import BaseObject
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.tracing.ranking.common.trace_layer import TraceLayer


@dataclass
class ApiDefinition(BaseObject):
    """
    Defines the dataset received through the API.
    """
    artifacts: List[Artifact]
    layers: List[TraceLayer]
    links: List[TracePredictionEntry] = None
    summary: str = None

    def get_links(self) -> List[TracePredictionEntry]:
        """
        :return: Returns the trace links defined in API dataset.
        """
        return [] if self.links is None else self.links
