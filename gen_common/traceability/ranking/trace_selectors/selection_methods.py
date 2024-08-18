from gen_common.traceability.ranking.trace_selectors.select_by_threshold import SelectByThreshold
from gen_common.traceability.ranking.trace_selectors.select_by_top_parents import SelectByTopParents
from gen_common.traceability.ranking.trace_selectors.selection_by_threshold_scaled_by_artifact import \
    SelectByThresholdScaledByArtifacts
from gen_common.util.supported_enum import SupportedEnum


class SupportedSelectionMethod(SupportedEnum):
    SELECT_BY_THRESHOLD = SelectByThreshold
    SELECT_TOP_PARENTS = SelectByTopParents
    SELECT_BY_THRESHOLD_SCALED = SelectByThresholdScaledByArtifacts
