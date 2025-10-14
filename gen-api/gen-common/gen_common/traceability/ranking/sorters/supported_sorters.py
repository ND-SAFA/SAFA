from gen_common.traceability.ranking.sorters.combined_sorter import CombinedSorter
from gen_common.traceability.ranking.sorters.transformer_sorter import TransformerSorter
from gen_common.traceability.ranking.sorters.vsm_sorter import VSMSorter
from gen_common.util.supported_enum import SupportedEnum


class SupportedSorter(SupportedEnum):
    VSM = VSMSorter
    TRANSFORMER = TransformerSorter
    COMBINED = CombinedSorter
