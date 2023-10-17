from typing import Optional, TypedDict


class Artifact(TypedDict):
    """
    Typed entity representing single artifact entry.
    """
    id: str
    content: str
    layer_id: str
    summary: Optional[str]
