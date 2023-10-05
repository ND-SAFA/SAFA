from enum import auto

from tgen.common.util.supported_enum import SupportedEnum


class SupportedSelectionMethod(SupportedEnum):
    FILTER_BY_THRESHOLD = auto()
    SELECT_TOP_PARENTS = auto()
