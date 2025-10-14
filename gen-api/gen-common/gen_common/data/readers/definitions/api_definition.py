from dataclasses import dataclass, field
from typing import Dict, List

from gen_common.data.objects.artifact import Artifact
from gen_common.data.objects.trace import Trace
from gen_common.data.objects.trace_layer import TraceLayer
from gen_common.infra.base_object import BaseObject


@dataclass
class ApiDefinition(BaseObject):
    """
    Defines the dataset received through the API.
    """
    artifacts: List[Artifact]
    layers: List[TraceLayer] = field(default_factory=list)
    links: List[Trace] = field(default_factory=list)
    summary: str = None

    def get_links(self) -> List[Trace]:
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
            links_param.append(Trace(**link))
        for layer in layers:
            layers_param.append(TraceLayer(**layer))
        return ApiDefinition(artifacts=artifacts_param, links=links_param, layers=layers_param, **additional_params)
