from gen_common.util.enum_util import FunctionalWrapper
from gen_common.util.supported_enum import SupportedEnum


class SupportedComparisonFunction(SupportedEnum):
    """
    Represents the different ways to compare metrics scores.
    Note, this is not an enum because functional wrapper break deepcopy method.
    """
    MAX = FunctionalWrapper(lambda a, b: b is None or a > b)
    MIN = FunctionalWrapper(lambda a, b: b is None or a < b)
