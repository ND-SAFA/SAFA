from dataclasses import dataclass
from typing import TypedDict


@dataclass
class TraceLayer(TypedDict):
    """
    Identifies a layer being traced.
    """
    parent: str
    child: str
