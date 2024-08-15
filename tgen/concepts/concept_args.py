from dataclasses import dataclass, field
from typing import List

from common_resources.data.objects.artifact import Artifact
from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context
from common_resources.tools.state_management.args import Args
from common_resources.tools.util.dataclass_util import required_field

from tgen_test.concepts.constants import CONCEPT_TYPE


@dataclass
class ConceptArgs(Args):
    """
    :param artifact_df: ArtifactDataFrame containing all concepts and query artifacts.
    :param concept_layer_id: Artifact type associated with project concepts.
    :param query_ids: Artifact Ids to match concepts against.
    :param llm_manager: LLM Manager used to complete prompts
    """
    query_ids: List[str] = required_field(field_name="Query ids")
    concept_layer_id: str = CONCEPT_TYPE
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    n_concepts_in_prompt: int = 30

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
