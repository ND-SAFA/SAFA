from enum import auto

from common_resources.tools.util.supported_enum import SupportedEnum


class SpecialDocTypes(SupportedEnum):
    API_DATAFLOW = "API DATAFLOW"
    DB_ENTITY_SPEC = "DB ENTITY SPEC"


class DocTypeConstraints(SupportedEnum):
    ONE_TARGET_PER_SOURCE = auto()
    USE_SOURCE_CONTEXT = auto()


DOC_TYPE2CONSTRAINTS = {SpecialDocTypes.API_DATAFLOW.value: {DocTypeConstraints.ONE_TARGET_PER_SOURCE,
                                                             DocTypeConstraints.USE_SOURCE_CONTEXT},
                        SpecialDocTypes.DB_ENTITY_SPEC.value: {DocTypeConstraints.ONE_TARGET_PER_SOURCE,
                                                               DocTypeConstraints.USE_SOURCE_CONTEXT}
                        }
