from dataclasses import dataclass, field
from typing import List

from gen_common.data.objects.trace import Trace

from gen.concepts.types.concept_match import ConceptMatch
from gen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from gen.concepts.types.entity_matching_pred import EntityMatchingPred
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.pipeline.state import State


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
    predicted_matches: List[Trace] = field(default_factory=lambda: [])
    """
    Final response of pipeline.
    """
    response: ConceptPipelineResponse = None
