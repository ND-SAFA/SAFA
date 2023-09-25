from dataclasses import dataclass
from typing import List, Dict

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

    @staticmethod
    def from_dict(artifacts: List[Dict], links: List[Dict], layers: List[Dict], **additional_params) -> "ApiDefinition":
        """
        Reads the api definition from dictionaries
        :param artifacts: The list of artifacts where the artifacts are stored as dicts
        :param links: The list of links where the links are stored as dicts
        :param layers: The list of layers where the layers are stored as dicts
        :param additional_params: Any other params (e.g. summary)
        :return: The ApiDefinition obj
        """
        artifacts_param, links_param, layers_param = [], [], []
        for artifact in artifacts:
            artifacts_param.append(Artifact(**artifact))
        for link in links:
            links_param.append(TracePredictionEntry(**link))
        for layer in layers:
            layers_param.append(TraceLayer(**layer))
        return ApiDefinition(artifacts=artifacts_param, links=links_param, layers=layers_param, **additional_params)
