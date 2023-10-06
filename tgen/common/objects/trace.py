from typing import TypedDict, Optional


class Trace(TypedDict):
    """
    A trace prediction for a pair of artifacts.
    """
    id: Optional[int]
    source: str
    target: str
    score: Optional[float]
    label: Optional[int]
    explanation: Optional[str]
