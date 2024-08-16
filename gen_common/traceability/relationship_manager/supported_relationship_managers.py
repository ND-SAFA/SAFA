from gen_common.traceability.relationship_manager.cross_encoder_manager import CrossEncoderManager
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.supported_enum import SupportedEnum


class SupportedRelationshipManager(SupportedEnum):
    EMBEDDING = EmbeddingsManager
    CROSS_ENCODER = CrossEncoderManager
