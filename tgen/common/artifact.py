from typing import Optional, TypedDict


class Artifact(TypedDict):
    """
    Typed entity representing single artifact entry.
    """
    id: str
    content: str
    summary: Optional[str]
    layer_id: str
