from dataclasses import dataclass, field
from typing import List

from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.concepts.types.entity_matching_pred import EntityMatchingPred
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.pipeline.state import State


@dataclass
class ConceptState(State):
    """
    Contains all concept artifacts.
    """
    concept_df: ArtifactDataFrame = None
    """
    List of concepts found directly in target artifact.
    """
    direct_matches: List[ConceptMatch] = field(default_factory=lambda: [])
    """
    List of entities extracted from artifact.
    """
    entity_data_frames: List[ArtifactDataFrame] = None
    """"
    List of predicted links between entities and concepts.
    """
    predicted_matches: List[EntityMatchingPred] = field(default_factory=lambda: [])
    """
    Final response of pipeline.
    """
    response: ConceptPipelineResponse = None
