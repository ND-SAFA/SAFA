from dataclasses import dataclass, field

from tgen.common.constants.model_constants import get_best_default_llm_manager_short_context
from tgen.common.objects.artifact import Artifact
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class ConceptArgs(PipelineArgs):
    """"
    LLM Manager used to complete prompts
    """
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_short_context)
    """
    DataFrame containing only concepts to match.
    """
    concept_df: ArtifactDataFrame = None
    """
    Artifact to match concepts against.
    """
    artifact: Artifact = None
    """
    Layer ID to given extracted entities.
    """
    entity_layer_id = "Entity"

    def __post_init__(self) -> None:
        """
        Verifies that required arguments are passed in.
        :return: None
        """

        if self.concept_df is None:
            raise Exception("Expected concepts to be defined.")
        if self.artifact is None:
            raise Exception("Expected artifact to be defined.")
