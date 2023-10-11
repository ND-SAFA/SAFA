from tgen.common.util.supported_enum import SupportedEnum
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.selectors.select_by_top_parents import SelectByTopParents
from tgen.tracing.ranking.selectors.selection_by_threshold_normalized_children import SelectByThresholdNormalizedChildren


class SupportedSelectionMethod(SupportedEnum):
    SELECT_BY_THRESHOLD = SelectByThreshold
    SELECT_BY_THRESHOLD_NORMALIZED_CHILDREN = SelectByThresholdNormalizedChildren
    SELECT_TOP_PARENTS = SelectByTopParents
