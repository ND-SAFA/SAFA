from typing import TypedDict, List, Dict


class SummaryResponse(TypedDict):
    """
    The response for a project summary request.
    """
    summary: str
    artifacts: List[Dict]
