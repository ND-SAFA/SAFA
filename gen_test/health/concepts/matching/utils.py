import pandas as pd
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset

from gen.health.concepts.concept_args import ConceptArgs
from gen_test.health.concepts.matching.constants import CONCEPT_TARGET_LAYER_ID, CONCEPT_TYPE
from gen_test.res.paths import GEN_TEST_PROJECT_CONCEPTS_CONCEPTS_PATH, GEN_TEST_PROJECT_CONCEPTS_REQUIREMENTS_PATH


def create_concept_args() -> ConceptArgs:
    """
    Creates ConceptArgs with test artifact and concepts.
    :return: ConceptArgs.
    """
    concept_df = _read_concept_df()
    query_df = _read_requirement_df()
    artifact_df = ArtifactDataFrame.concat(concept_df, query_df)
    trace_dataset = TraceDataset(artifact_df=artifact_df,
                                 trace_df=TraceDataFrame(),
                                 layer_df=LayerDataFrame())
    args = ConceptArgs(dataset=PromptDataset(trace_dataset=trace_dataset),
                       query_ids=query_df.index.tolist(),
                       concept_layer_id=CONCEPT_TYPE)
    return args


def _read_concept_df() -> ArtifactDataFrame:
    """
    :return: Reads concept data frame for test project.
    """
    concept_df = pd.read_csv(GEN_TEST_PROJECT_CONCEPTS_CONCEPTS_PATH)
    concept_df[ArtifactKeys.LAYER_ID.value] = CONCEPT_TYPE
    concept_df = ArtifactDataFrame(concept_df)
    return concept_df


def _read_requirement_df() -> ArtifactDataFrame:
    """
    :return:the target requirements as artifacts.
    """
    requirement_df = pd.read_csv(GEN_TEST_PROJECT_CONCEPTS_REQUIREMENTS_PATH)
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
