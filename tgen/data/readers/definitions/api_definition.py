from dataclasses import dataclass
from typing import Dict, List, Tuple

from tgen.util.base_object import BaseObject


@dataclass
class ApiDefinition(BaseObject):
    """
    Defines the dataset received through the API.
    """
    artifact_layers: Dict[str, str]
    layers: List[Tuple[str, str]]
    true_links: List[Tuple[str, str]] = None

    def get_links(self) -> List[Tuple[str, str]]:
        """
        :return: Returns the trace links defined in API dataset.
        """
        return [] if self.true_links is None else self.true_links
