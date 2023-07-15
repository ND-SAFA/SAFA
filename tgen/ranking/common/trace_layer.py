from dataclasses import dataclass


@dataclass
class TraceLayer:
    """
    Identifies a layer being traced.
    """
    parent: str
    child: str
