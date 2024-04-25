from typing import Dict, List

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.embeddings.embeddings_manager import EmbeddingsManager


def embedding_tracer(state: Dict, source_artifact: List[str], target_artifact: List[str]):
    if "embeddings_manager" not in state:
        state["embeddings_manager"] = EmbeddingsManager.create_from_content(source_artifact,
                                                                            model_name=SMALL_EMBEDDING_MODEL,
                                                                            show_progress_bar=True)
        state["source_embeddings"] = [state["embeddings_manager"].get_embedding(c) for c in source_artifact]
    embeddings_manager = state["embeddings_manager"]
    source_embeddings = state["source_embeddings"]

    return calculate_similarities(embeddings_manager, source_embeddings, target_artifact)


def calculate_similarities(embeddings_manager, question_embeddings, layer_artifacts: List[str]):
    layer_artifact_embeddings = []
    for artifact in layer_artifacts:
        artifact_embedding = embeddings_manager.update_or_add_content(artifact,
                                                                      artifact,
                                                                      create_embedding=True)
        layer_artifact_embeddings.append(artifact_embedding)
    similarity_matrix = EmbeddingUtil.calculate_similarities(question_embeddings, layer_artifact_embeddings)
    return similarity_matrix
