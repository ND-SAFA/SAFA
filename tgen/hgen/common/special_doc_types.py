from tgen.common.util.supported_enum import SupportedEnum


class SpecialDocTypes(SupportedEnum):
    API_DATAFLOW = "API DATAFLOW"


ONE_TARGET_PER_SOURCE_DOC_TYPES = {SpecialDocTypes.API_DATAFLOW.value}
USE_CONTEXT_DOC_TYPES = {SpecialDocTypes.API_DATAFLOW.value}
