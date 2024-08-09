from typing import Optional

from common_resources.tools.util.typed_enum_dict import TypedEnumDict
from common_resources.data.keys.structure_keys import TraceKeys


class Trace(TypedEnumDict, keys=TraceKeys):
    """
    A trace prediction for a pair of artifacts.
    """
    link_id: Optional[int]
    source: str
    target: str
    score: Optional[float]
    label: Optional[int]
    explanation: Optional[str]
