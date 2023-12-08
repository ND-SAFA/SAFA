from enum import auto

from tgen.common.util.supported_enum import SupportedEnum


class SupportedSeedClusteringMethods(SupportedEnum):
    """
    Enumerates all supporting clustering methods.
    """
    CENTROID_CHOOSES_ARTIFACTS = auto()
    ARTIFACTS_CHOOSE_CENTROIDS = auto()
