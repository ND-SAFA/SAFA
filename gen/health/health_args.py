from dataclasses import dataclass, field
from typing import List

from gen_common.constants.default_model_managers import get_best_default_llm_manager_long_context
from gen_common.data.objects.artifact import Artifact
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.pipeline.args import Args
from gen_common.util.dataclass_util import required_field

from gen_test.health.concepts.matching.constants import CONCEPT_TYPE


@dataclass
class HealthArgs(Args):
    """
    :param concept_layer_id: Artifact type associated with project concepts.
    :param query_ids: Artifact Ids to match concepts against.
    :param llm_manager: LLM Manager used to complete prompts
    """
    query_ids: List[str] = required_field(field_name="Query ids")
    concept_layer_id: str = CONCEPT_TYPE
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    # concept-matching
    n_concepts_in_prompt: int = 30
    context_doc_path: str = None

    _query_artifacts: List[Artifact] = None
    _concept_artifacts: List[Artifact] = None

    def get_query_artifacts(self) -> List[Artifact]:
        """
        :return: Returns query artifacts.
        """
        if self._query_artifacts is None:
            self._query_artifacts = self.dataset.artifact_df.filter_by_index(self.query_ids).to_artifacts()
        return self._query_artifacts

    def get_concept_artifacts(self) -> List[Artifact]:
        """
        :return: Returns the concept artifacts.
        """
        if self._concept_artifacts is None:
            self._concept_artifacts = self.dataset.artifact_df.get_artifacts_by_type(self.concept_layer_id).to_artifacts()
        return self._concept_artifacts
