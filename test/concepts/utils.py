import pandas as pd

from test.concepts.constants import CONCEPT_ARTIFACT_ID, CONCEPT_ARTIFACT_PATH, CONCEPT_DF_PATH, CONCEPT_ENTITIES, \
    CONCEPT_TARGET_LAYER_ID, CONCEPT_TYPE
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys


def create_concept_args() -> ConceptArgs:
    """
    Creates ConceptArgs with test artifact and concepts.
    :return: ConceptArgs.
    """
    artifact_content = FileUtil.read_file(CONCEPT_ARTIFACT_PATH)
    raw_df = pd.read_csv(CONCEPT_DF_PATH)
    raw_df[ArtifactKeys.LAYER_ID.value] = CONCEPT_TYPE
    concept_df = ArtifactDataFrame(raw_df)
    target_artifact: Artifact = Artifact(
        id=CONCEPT_ARTIFACT_ID,
        content=artifact_content,
        layer_id=CONCEPT_TARGET_LAYER_ID,
        summary=""
    )
    args = ConceptArgs(concept_df=concept_df, artifact=target_artifact)
    return args


def create_concept_test_entities() -> ArtifactDataFrame:
    """
    Creates list of test entities.
    :return: Entities.
    """
    entities = []
    for e_name, e_desc in CONCEPT_ENTITIES.items():
        entities.append(Artifact(id=e_name, content=e_desc, layer_id="Entity", summary=""))
    return ArtifactDataFrame(entities)
