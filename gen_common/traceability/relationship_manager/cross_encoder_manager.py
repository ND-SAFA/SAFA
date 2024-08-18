from typing import Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from gen_common.constants.environment_constants import DEFAULT_CROSS_ENCODER_MODEL
from gen_common.constants.hugging_face_constants import DEFAULT_ENCODING_BATCH_SIZE
from gen_common.llm.model_properties import ModelTask
from gen_common.traceability.relationship_manager.abstract_relationship_manager import AbstractRelationshipManager
from gen_common.util.list_util import ListUtil


class CrossEncoderManager(AbstractRelationshipManager):
    MODEL_MAP = {}

    def __init__(self, content_map: Dict[str, str] = None, model_name: str = DEFAULT_CROSS_ENCODER_MODEL,
                 model: SentenceTransformer = None, show_progress_bar: bool = True):
        """
        Initializes the manager with the content used to predict using a given cross encoder.
        :param content_map: Maps id to the corresponding content.
        :param model_name: Name of model to use as the cross encoder.
        :param model: The model to use to embed artifacts.
        :param show_progress_bar: Whether to show progress bar when calculating batches.
        """
        super().__init__(model_name=model_name, show_progress_bar=show_progress_bar, content_map=content_map, model=model,
                         model_type=ModelTask.CROSS_ENCODER.name)

    def _compare_artifacts(self, ids1: List[str], ids2: List[str], include_ids: bool = False, **kwargs) -> np.array:
        """
        Calculates the similarities between two sets of artifacts.
        :param ids1: List of ids to compare with ids2.
        :param ids2: List of ids to compare with ids1.
        :param include_ids: If True, includes the ids in the content for scoring.
        :return: The scores between each artifact in ids1 with those in ids2 in a similarity matrix.
        """
        pairs = [(id1, id2) for id1 in ids1 for id2 in ids2]
        scores = iter(self.calculate_scores(pairs, include_ids))
        similarity_matrix = np.empty((len(ids1), len(ids2)))
        for i, id1 in enumerate(ids1):
            for j, id2 in enumerate(ids2):
                similarity_matrix[i, j] = next(scores)
        return similarity_matrix

    def calculate_scores(self, id_pairs: List[Tuple[str, str]], include_ids: bool = False) -> List[float]:
        """
        Calculates the relationship score between each artifact pair..
        :param id_pairs: List of tuples of id pairs to compare.
        :param include_ids: If True, includes the ids in the content for scoring.
        :return: A list of scores corresponding to each pair comparison.
        """
        batch_size = DEFAULT_ENCODING_BATCH_SIZE
        ids1, ids2 = ListUtil.unzip(id_pairs)
        artifact_content1 = self.get_artifact_contents(ids1, include_ids=include_ids)
        artifact_content2 = self.get_artifact_contents(ids2, include_ids=include_ids)
        artifact_combinations = [[artifact_content1[i], artifact_content2[i]]
                                 for i, (id1, id2) in enumerate(id_pairs) if not self.relationship_exists(id1, id2)]
        show_progress_bar = self._determine_show_progress_bar(artifact_combinations, "Calculating sim scores for artifacts...",
                                                              batch_size)
        scores = self.get_model().predict(artifact_combinations, batch_size=batch_size, show_progress_bar=show_progress_bar)
        scores = iter(scores)
        all_scores = []
        for id1, id2 in id_pairs:
            score = self.get_relationship(id1, id2) if self.relationship_exists(id1, id2) else next(scores)
            all_scores.append(score)
        return all_scores
