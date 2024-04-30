import os
from typing import List

from tgen.common.objects.artifact import Artifact
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.testres.paths.paths import TEST_DATA_DIR

CONCEPT_ARTIFACT_ID = "GSFPS-3221"
CONCEPT_TARGET_LAYER_ID = "Requirement"
CONCEPT_DATA_PATH = os.path.join(TEST_DATA_DIR, "concepts")
CONCEPT_DF_PATH = os.path.join(CONCEPT_DATA_PATH, "Concept.csv")
CONCEPT_ARTIFACT_PATH = os.path.join(CONCEPT_DATA_PATH, "requirement.txt")
CONCEPT_TYPE = "Concept"
CONCEPT_ENTITY_MATCHED = "GS"
CONCEPT_ENTITY_UNDEFINED = "IFDS"


class ConceptData:
    """
    # Test Case

    List of concepts scraped from NASA dataset: https://dev.safa.ai/project?version=1314a50e-3b09-4197-9264-61e6ce6d3de5
    Artificially added Concept `GS: Ground Speed` to conflict with concept `Ground Station (GS)`
    There are 4 direct matches present above with those above, `Command` and `Telemetry (TLM)` appear naturally in the target artifact.

    During entity extraction, three entities are mocked list below as E1, E2, and, E3. E1 is meant to be a multi-match
    to the concepts `GS: Ground Speed` and `Ground Station (GS)` so only  `Command` and `Telemetry (TLM)` are  valid matches.
    E2 is used to mock a predicted link to the concept C5. E3 is artificially introduced to trigger an undefined concept.

    Finally in entity concept matching, two predictions are mocked. First, we duplicate the direct matches to GS family of concepts to
    test that these are filtered out if they have been addressed by the direct matching method. Second, we mock a valid prediction
    between E2 and C5 which is expected to make it to the final response.

    # Children
    - Expected: Test Case Expectations as constants.
    - LayerId: Artifacts types used to identify concepts and construct entities in pipeline.
    - Entities: Entities referenced in test suite.
    - Concepts: Concepts referenced in test suite.
    """

    class Expected:
        """
        - N_DIRECT_MATCHES: 4 direct matches but only 2 unique and other 2 are dups
        - N_MULTI_MATCHES: GS -> Ground Station + Ground Speed
        - MULTI_MATCH_LOC: 4  # 'GS' @ 4
        - N_PREDICTED_MATCHES: E2 is predicted to match with C5 (mocked, this would have been caught in direct matching if present)
        - N_UNDEFINED: IFDS/E3 is not in concepts and marked as undefined.
        """
        N_DIRECT_MATCHES = 2
        N_MULTI_MATCHES = 1
        MULTI_MATCH_LOC = 4
        N_PREDICTED_MATCHES = 1
        N_UNDEFINED = 1

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

    class LayerId:
        """
        - CONCEPT: Used to fill in layer_id in test concepts @  CONCEPT_DF_PATH
        - ENTITY: Layer ID for entity found in an artifact.
        """
        CONCEPT = "Concept"
        ENTITY = "Entity"

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
