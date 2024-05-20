from typing import Optional

from tgen.common.util.typed_enum_dict import TypedEnumDict
from tgen.data.keys.structure_keys import TraceKeys


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
