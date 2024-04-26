import os

from tgen.testres.paths.paths import TEST_DATA_DIR

CONCEPT_ARTIFACT_ID = "GSFPS-3221"
CONCEPT_TARGET_LAYER_ID = "Requirement"
CONCEPT_DATA_PATH = os.path.join(TEST_DATA_DIR, "concepts")
CONCEPT_DF_PATH = os.path.join(CONCEPT_DATA_PATH, "concept.csv")
CONCEPT_ARTIFACT_PATH = os.path.join(CONCEPT_DATA_PATH, "requirement.txt")
CONCEPT_TYPE = "Concept"
CONCEPT_ENTITY_MATCHED = "GS"
CONCEPT_ENTITY_UNDEFINED = "IFDS"
CONCEPT_ENTITIES = {
    CONCEPT_ENTITY_MATCHED: "Ground Segment",
    CONCEPT_ENTITY_UNDEFINED: "Intermediate Frequency Distribution System"
}
