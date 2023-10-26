import math
import random

import numpy as np

from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class DetectDuplicateArtifacts(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        embeddings_manager = state.embedding_manager

        new_artifact_map = {i: content for i, content in enumerate(state.refined_content)}
        new_artifact_embeddings_map = embeddings_manager.update_or_add_contents(new_artifact_map, create_embedding=True)
        new_artifact_ids = list(new_artifact_embeddings_map.keys())
        new_artifact_embeddings = list(new_artifact_embeddings_map.values())

        similarity_matrix = EmbeddingUtil.calculate_similarities(new_artifact_embeddings, new_artifact_embeddings)

        indices = np.argwhere(similarity_matrix > 0.75)
        max_index = math.ceil(len(new_artifact_ids) / 2)
        filtered_indices = [(i, j) for i, j in indices if i != j and i < max_index]

        dup_set = set()
        dup_counter = {}
        for source_index, target_index in filtered_indices:
            source_artifact_id = new_artifact_ids[source_index]
            target_artifact_id = new_artifact_ids[target_index]

            if source_artifact_id not in dup_counter:
                dup_counter[source_artifact_id] = 0
            if target_artifact_id not in dup_counter:
                dup_counter[target_artifact_id] = 0

            dup_set.add((source_artifact_id, target_artifact_id))
            dup_counter[source_artifact_id] += 1
            dup_counter[target_artifact_id] += 1

        duplicate_artifact_ids = set([a_id for a_id, count in dup_counter.items() if count > 1])
        dup_set = [(s, t) for s, t in dup_set if s not in duplicate_artifact_ids and t not in duplicate_artifact_ids]
        for index_tuple in dup_set:
            k = random.randint(0, 1)  # decide on k once
            artifact_to_remove = index_tuple[k]
            duplicate_artifact_ids.add(artifact_to_remove)
        logger.info(f"Removing: {len(duplicate_artifact_ids)} duplicates.")

        refined_content = {}
        for i, (k, v) in enumerate(state.refined_content.items()):
            if i not in duplicate_artifact_ids:
                refined_content[k] = v
        state.refined_content = refined_content
