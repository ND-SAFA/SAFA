import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

from tgen.common.constants.hugging_face_constants import DEFAULT_ENCODING_BATCH_SIZE
from tgen.common.constants.ranking_constants import DEFAULT_CROSS_ENCODER_MODEL
from tgen.models.model_properties import ModelTask
from tgen.relationship_manager.abstract_relationship_manager import AbstractRelationshipManager


class CrossEncoderManager(AbstractRelationshipManager):
    MODEL_MAP = {}

    def __init__(self, content_map: Dict[str, str], model_name: str = DEFAULT_CROSS_ENCODER_MODEL, model: SentenceTransformer = None,
                 show_progress_bar: bool = True):
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
        scores = iter(self.__calculate_scores(ids1, ids2, include_ids))
        similarity_matrix = np.empty((len(ids1), len(ids2)))
        for i, id1 in enumerate(ids1):
            for j, id2 in enumerate(ids2):
                score = self.get_relationship(id1, id2) if self.relationship_exists(id1, id2) else next(scores)
                similarity_matrix[i, j] = score
        return similarity_matrix

    def __calculate_scores(self, ids1: List[str], ids2: List[str], include_ids: bool = False) -> List[float]:
        """
        Calculates the relationship score between each artifact in ids1 and id2.
        :param ids1: List of ids to compare with ids2.
        :param ids2: List of ids to compare with ids1.
        :param include_ids: If True, includes the ids in the content for scoring.
        :return: A list of scores corresponding to each pair comparison.
        """
        batch_size = DEFAULT_ENCODING_BATCH_SIZE
        artifact_contents1 = self.get_artifact_contents(ids1, include_ids)
        artifact_contents2 = self.get_artifact_contents(ids2, include_ids)
        artifact_combinations = [[artifact_contents1[i], artifact_contents2[j]] for i, id1 in enumerate(ids1)
                                 for j, id2 in enumerate(ids2) if not self.relationship_exists(id1, id2)]
        show_progress_bar = self._determine_show_progress_bar(artifact_combinations, "Calculating sim scores for artifacts...",
                                                              batch_size)
        scores = self.get_model().predict(artifact_combinations, batch_size=batch_size, show_progress_bar=show_progress_bar)
        return scores
