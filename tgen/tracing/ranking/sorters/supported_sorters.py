from tgen.common.util.supported_enum import SupportedEnum
from tgen.tracing.ranking.sorters.combined_sorter import CombinedSorter
from tgen.tracing.ranking.sorters.transformer_sorter import TransformerSorter
from tgen.tracing.ranking.sorters.vsm_sorter import VSMSorter


class SupportedSorter(SupportedEnum):
    VSM = VSMSorter
    TRANSFORMER = TransformerSorter
    COMBINED = CombinedSorter
