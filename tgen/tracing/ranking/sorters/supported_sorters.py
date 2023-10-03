from tgen.common.util.enum_util import FunctionalWrapper
from tgen.common.util.supported_enum import SupportedEnum
from tgen.tracing.ranking.sorters.embedding_sorter import embedding_sorter
from tgen.tracing.ranking.sorters.vsm_sorter import vsm_sorter


class SupportedSorter(SupportedEnum):
    VSM = FunctionalWrapper(vsm_sorter)
    EMBEDDING = FunctionalWrapper(embedding_sorter)
