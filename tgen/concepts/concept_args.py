from dataclasses import dataclass

from tgen.common.objects.artifact import Artifact
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class ConceptArgs(PipelineArgs):
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
