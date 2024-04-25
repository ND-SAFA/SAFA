import numpy as np

from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState


class GroupChunks(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        ps_section = "Sub-systems"

        artifact_map = state.artifact_map
        artifact_ids = artifact_map.keys()
        parent2children = state.sorted_parent2children

        chunks = list(set(state.project_summary[ps_section]["chunks"]))
        chunk_map = {c: c for c in chunks}
        chunk_embeddings = list(state.embedding_manager.update_or_add_contents(chunk_map, create_embedding=True).values())
        artifact_embeddings = state.embedding_manager.get_embeddings(artifact_ids)

        similarity_matrix = EmbeddingUtil.calculate_similarities(chunk_embeddings, artifact_embeddings)

        chunk2artifact = {}
        for i, a_id in enumerate(artifact_ids):
            scores_to_chunks = similarity_matrix[:, i]
            chunk_index = np.argmax(scores_to_chunks)
            top_chunk = chunks[chunk_index]
            if top_chunk not in chunk2artifact:
                chunk2artifact[top_chunk] = []
            chunk2artifact[top_chunk].append(a_id)

        print("Hi")
