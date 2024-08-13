from common_resources.tools.util.supported_enum import SupportedEnum
from tgen.relationship_manager.cross_encoder_manager import CrossEncoderManager
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager


class SupportedRelationshipManager(SupportedEnum):
    EMBEDDING = EmbeddingsManager
    CROSS_ENCODER = CrossEncoderManager
