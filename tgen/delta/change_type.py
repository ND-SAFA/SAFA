from enum import Enum, auto
from typing import Union

from tgen.common.util.enum_util import EnumUtil


class ChangeType(Enum):
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    RENAMED = "renamed"
