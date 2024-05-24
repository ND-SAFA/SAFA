from tgen.common.util.supported_enum import SupportedEnum
from tgen.tracing.ranking.trace_selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.trace_selectors.select_by_top_parents import SelectByTopParents
from tgen.tracing.ranking.trace_selectors.selection_by_threshold_scaled_by_artifact import SelectByThresholdScaledByArtifacts


class SupportedSelectionMethod(SupportedEnum):
    SELECT_BY_THRESHOLD = SelectByThreshold
    SELECT_TOP_PARENTS = SelectByTopParents
    SELECT_BY_THRESHOLD_SCALED = SelectByThresholdScaledByArtifacts
