from dataclasses import dataclass

from common_resources.tools.util.base_object import BaseObject


@dataclass
class TraceLayer(BaseObject):
    """
    Identifies a layer being traced.
    """
    parent: str
    child: str
