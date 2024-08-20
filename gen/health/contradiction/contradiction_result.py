from typing import List, TypedDict


class ContradictionsResult(TypedDict):
    conflicting_ids: List[str]
    explanation: str
