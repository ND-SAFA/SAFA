from typing import Dict, Tuple

from tgen.common.util.logging.logger_manager import logger
from tgen.hgen.common.duplicate_detector import DuplicateDetector
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep

CountMap = Dict[str, int]
MatrixIndex = Tuple[int, int]
ArtifactPair = Tuple[str, str]


class DetectDuplicateArtifacts(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Removes duplicate generated artifacts.
        :param args: The arguments to HGEN pipeline.
        :param state: The state of the
        :return: None
        """

        embeddings_manager = state.embedding_manager

        new_artifact_map = {i: content for i, content in enumerate(state.refined_content)}  # Will the ID be unique??
        new_artifact_embeddings_map = embeddings_manager.update_or_add_contents(new_artifact_map, create_embedding=True)
        new_artifact_ids = list(new_artifact_embeddings_map.keys())

        duplicate_detector = DuplicateDetector(embeddings_manager, duplicate_similarity_threshold=args.duplicate_similarity_threshold)
        duplicate_artifact_ids = duplicate_detector.get_duplicates(new_artifact_ids)

        logger.info(f"Removing: {len(duplicate_artifact_ids)} duplicates.")

        refined_content = {}
        for i, (artifact_id, artifact_content) in enumerate(state.refined_content.items()):
            if i not in duplicate_artifact_ids:
                refined_content[artifact_id] = artifact_content
        state.refined_content = refined_content
