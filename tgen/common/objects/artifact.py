from typing import Optional

from tgen.common.util.typed_enum_dict import TypedEnumDict
from tgen.data.keys.structure_keys import ArtifactKeys


class Artifact(TypedEnumDict, keys=ArtifactKeys):
    """
    Typed entity representing single artifact entry.
    """
    id: str
    content: str
    layer_id: str
    summary: Optional[str]
