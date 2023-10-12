from tgen.common.util.supported_enum import SupportedEnum
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingSorter
from tgen.tracing.ranking.sorters.vsm_sorter import VSMSorter


class SupportedSorter(SupportedEnum):
    VSM = VSMSorter
    EMBEDDING = EmbeddingSorter
