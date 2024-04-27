import os
from typing import List

from tgen.common.objects.artifact import Artifact
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.testres.paths.paths import TEST_DATA_DIR

CONCEPT_ARTIFACT_ID = "GSFPS-3221"
CONCEPT_TARGET_LAYER_ID = "Requirement"
CONCEPT_DATA_PATH = os.path.join(TEST_DATA_DIR, "concepts")
CONCEPT_DF_PATH = os.path.join(CONCEPT_DATA_PATH, "concept.csv")
CONCEPT_ARTIFACT_PATH = os.path.join(CONCEPT_DATA_PATH, "requirement.txt")
CONCEPT_TYPE = "Concept"
CONCEPT_ENTITY_MATCHED = "GS"
CONCEPT_ENTITY_UNDEFINED = "IFDS"


class ConceptData:
    """

    - LayerId: Defines artifacts types used to identify concepts and construct entities in pipeline.
    - Entities: Defines the three entities that are extracted from the artifact.
    """

    class LayerId:
        """
        - CONCEPT: Used to fill in layer_id in test concepts @  CONCEPT_DF_PATH
        - ENTITY: Layer ID for entity found in an artifact.
        """
        CONCEPT = "Concept"
        ENTITY = "Entity"

    class Entities:
        """
        - E1: Used to directly match to two different concepts (C1 and C2)
        - E2: Used as a predicted match.
        - E3: Used as an undefined match.
        """
        E1 = "GS"
        E2 = "Data Collection System"
        E3 = "IFDS"
        UNDEFINED = E3

    class Concepts:
        """
        - C1: Direct match to E1
        - C2: Direct match to E1
        - C3: Unexpected match, but kept.
        - C4: Used to test alternate name extraction
        - C5: Used as a predicted match to E2.
        """
        C1 = "Ground Station (GS)"
        C2 = "GS"
        C3 = "Command"
        C4 = "Telemetry (TLM)"
        C5 = "Data Collection System (DCS)"

    class Expected:
        N_DIRECT_MATCHES = 2  # 4 direct matches but only 2 unique and other 2 are dups
        N_MULTI_MATCHES = 1  # GS -> Ground Station + Ground Speed
        MULTI_MATCH_LOC = 4  # 'GS' @ 4
        N_PREDICTED_MATCHES = 1  # E2
        N_UNDEFINED = 1  # IFDS

    DirectMatches = [Concepts.C1, Concepts.C2, Concepts.C3, Concepts.C4]
    Predicted = [{"source": Entities.E1, "target": Concepts.C2}, {"source": Entities.E2, "target": Concepts.C5}]

    @staticmethod
    def get_entity_names() -> List[str]:
        """
        :return: List of entity names found in artifact.
        """
        return [ConceptData.Entities.E1, ConceptData.Entities.E2, ConceptData.Entities.E3]

    @staticmethod
    def get_entity_df() -> ArtifactDataFrame:
        """
        :return: DataFrame with entities as artifacts.
        """
        artifacts = [Artifact(id=e, content="description", layer_id=ConceptData.LayerId.ENTITY, summary="")
                     for e in ConceptData.get_entity_names()]
        return ArtifactDataFrame(artifacts)
