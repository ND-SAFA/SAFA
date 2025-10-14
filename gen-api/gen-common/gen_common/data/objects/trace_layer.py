from dataclasses import dataclass

from gen_common.infra.base_object import BaseObject


@dataclass
class TraceLayer(BaseObject):
    """
    Identifies a layer being traced.
    """
    parent: str
    child: str
