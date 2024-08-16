from typing import Optional

from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.util.typed_enum_dict import TypedEnumDict


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
