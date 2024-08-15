import pandas as pd
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset

from common_resources.data.objects.artifact import Artifact
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen_test.concepts.constants import CONCEPT_ARTIFACT_PATH, CONCEPT_DF_PATH, CONCEPT_TARGET_LAYER_ID, \
    CONCEPT_TYPE


def create_concept_args() -> ConceptArgs:
    """
    Creates ConceptArgs with test artifact and concepts.
    :return: ConceptArgs.
    """
    concept_df = _read_concept_df()
    query_df = create_query_artifacts()
    artifact_df = ArtifactDataFrame.concat(concept_df, query_df)
    args = ConceptArgs(dataset=PromptDataset(artifact_df=artifact_df),
                       query_ids=query_df.index.tolist(),
                       concept_layer_id=CONCEPT_TYPE)
    return args


def _read_concept_df() -> ArtifactDataFrame:
    """
    :return: Reads concept data frame for test project.
    """
    concept_df = pd.read_csv(CONCEPT_DF_PATH)
    concept_df[ArtifactKeys.LAYER_ID.value] = CONCEPT_TYPE
    concept_df = ArtifactDataFrame(concept_df)
    return concept_df


def create_query_artifacts() -> ArtifactDataFrame:
    """
    :return:the target requirements as artifacts.
    """
    requirement_df = pd.read_csv(CONCEPT_ARTIFACT_PATH)
    artifacts = []
    for i, row in requirement_df.iterrows():
        artifacts.append(
            Artifact(
                id=row["id"],
                content=row["content"],
                layer_id=CONCEPT_TARGET_LAYER_ID,
                summary=""
            )
        )
    return ArtifactDataFrame(artifacts)


def create_concept_state(args: ConceptArgs) -> ConceptState:
    """
    Creates ConceptState with concpt df.
    :return: ConceptState.
    """
    state = ConceptState(concept_df=args.dataset.artifact_df.get_artifacts_by_type(args.concept_layer_id))
    return state
