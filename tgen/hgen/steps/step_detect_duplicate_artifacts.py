import math

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

        indices = np.argwhere(similarity_matrix > 0.85)
        max_index = math.ceil(len(new_artifact_ids) / 2)
        filtered_indices = [(i, j) for i, j in indices if i != j and i < max_index]

        dup_pairs = set()
        dup_counter = {}
        for source_index, target_index in filtered_indices:
            source_artifact_id = new_artifact_ids[source_index]
            target_artifact_id = new_artifact_ids[target_index]

            if source_artifact_id not in dup_counter:
                dup_counter[source_artifact_id] = 0
            if target_artifact_id not in dup_counter:
                dup_counter[target_artifact_id] = 0

            dup_pairs.add((source_artifact_id, target_artifact_id))
            dup_counter[source_artifact_id] += 1
            dup_counter[target_artifact_id] += 1

        most_to_least_overlapping_dups = [d[0] for d in sorted(dup_counter.items(), key=lambda x: x[1], reverse=True)]
        fixed_dups = set()
        duplicate_artifact_ids = set()
        for dup_art in most_to_least_overlapping_dups:
            for dup_pair in dup_pairs:
                if dup_art in dup_pair and dup_pair not in fixed_dups:
                    fixed_dups.add(dup_pair)
                    duplicate_artifact_ids.add(dup_art)

        logger.info(f"Removing: {len(duplicate_artifact_ids)} duplicates.")

        refined_content = {}
        for i, (k, v) in enumerate(state.refined_content.items()):
            if i not in duplicate_artifact_ids:
                refined_content[k] = v
        state.refined_content = refined_content
