from common_resources.tools.util.supported_enum import SupportedEnum
from common_resources.traceability.relationship_manager.cross_encoder_manager import CrossEncoderManager
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager


class SupportedRelationshipManager(SupportedEnum):
    EMBEDDING = EmbeddingsManager
    CROSS_ENCODER = CrossEncoderManager
