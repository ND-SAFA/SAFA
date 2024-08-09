from typing import Tuple

from langchain_core.documents.base import Document

from common_resources.data.creators.prompt_dataset_creator import PromptDatasetCreator
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.graph.io.graph_args import GraphArgs
from common_resources.graph.io.graph_state import GraphState
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.param_specs import ParamSpecs
from common_resources_test.testprojects.prompt_test_project import PromptTestProject


def get_io_without_data(**kwargs):
    dataset_creator = PromptDatasetCreator(project_reader=PromptTestProject.get_artifact_project_reader())
    args = GraphArgs(dataset_creator=dataset_creator)
    return args, args.to_graph_input(**kwargs)


class PetData:
    ARTIFACT_CONTENT = ["All dogs are really cute.", "Cars make vroom vroom sound.", "Fire trucks are loud.",
                        "Dogs pee on fire hydrants.", "Cats are better than Dogs"]
    LAYER_ID1 = "facts"
    LAYER_ID2 = "things"
    CONTEXT_ARTIFACTS = [0, 1, 3, 4]

    @staticmethod
    def get_io(include_documents: bool = False, **kwargs) -> Tuple[GraphArgs, GraphState]:
        artifacts_df = ArtifactDataFrame({ArtifactKeys.ID: [f"a_{i}" for i, _ in enumerate(PetData.ARTIFACT_CONTENT)],
                                          ArtifactKeys.CONTENT: PetData.ARTIFACT_CONTENT,
                                          ArtifactKeys.LAYER_ID: [PetData.LAYER_ID1 if i % 2 == 0 else PetData.LAYER_ID2
                                                                  for i, _ in enumerate(PetData.ARTIFACT_CONTENT)]})
        dataset = PromptDataset(trace_dataset=TraceDataset(artifacts_df, TraceDataFrame(), LayerDataFrame()))
        if include_documents:
            DictUtil.update_kwarg_values(kwargs, documents=PetData.get_context_docs())
        params = ParamSpecs.create_from_method(GraphArgs.__init__).get_accepted_params(kwargs)
        kwargs = {k: v for k, v in kwargs.items() if k not in params}
        args = GraphArgs(dataset=dataset, **params)
        return args, args.to_graph_input(**kwargs)

    @staticmethod
    def get_context_docs():
        return {"best pet": [Document(PetData.ARTIFACT_CONTENT[i], metadata={ArtifactKeys.ID.value: f"a_{i}"}) for i in
                             PetData.CONTEXT_ARTIFACTS]}
