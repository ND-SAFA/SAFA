from typing import Optional, TypedDict


class Artifact(TypedDict):
    id: str
    content: str
    summary: Optional[str]
