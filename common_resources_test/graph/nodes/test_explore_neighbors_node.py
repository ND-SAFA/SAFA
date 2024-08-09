from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import TraceKeys, LayerKeys
from common_resources.data.objects.artifact import Artifact
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.graph.io.graph_args import GraphArgs
from common_resources.graph.nodes.explore_neighbors_node import ExploreNeighborsNode
from common_resources_test.base_tests.base_test import BaseTest


class TestExploreNeighborsNode(BaseTest):
    CONCEPT_LAYER_ID = "concepts"
    PET_LAYER_ID = "pets"
    FACTS_LAYER_ID = "facts"
    ARTIFACT_CONTENT = ["dogs", "cats",  # 0, 1
                        "Cat1: Michael", "Dog1: Scruffy", "Cat2: Meredith", "Dog2: Rocky",  # 2, 3, 4, 5
                        "Michael is quite fat", "Meredith bites a lot", "Rocky loves bubbles", "Scruffy has a toupee"]  # 6, 7, 8, 9
    ARTIFACT_IDS = [f"{i}" for i, _ in enumerate(ARTIFACT_CONTENT)]
    LAYER_IDS = [CONCEPT_LAYER_ID] * 2 + [PET_LAYER_ID] * 4 + [FACTS_LAYER_ID] * 4
    TRACES = {
        0: [3, 5],
        1: [2, 4],
        2: [6],
        3: [9],
        4: [7],
        5: [8],
    }

    def test_perform_action(self):
        selected_artifact_ids = {"1", "5"}
        args = GraphArgs(dataset=self.construct_dataset())
        state = args.to_graph_input(
            selected_artifact_ids=selected_artifact_ids)
        expected_relationships = {2, 4, 0, 8}
        updated_state = ExploreNeighborsNode(args).perform_action(state)
        context = updated_state["documents"]
        self.assertSetEqual(selected_artifact_ids, set(context.keys()))
        all_docs = [doc for a_id, docs in context.items() for doc in docs]
        self.assertEqual(len(all_docs), len(expected_relationships))
        for doc in all_docs:
            self.assertIn(int(doc.metadata["id"]), expected_relationships)

    def construct_dataset(self):
        trace_df = TraceDataFrame([{TraceKeys.child_label(): str(child), TraceKeys.parent_label(): str(parent), TraceKeys.LABEL: 1}
                                   for parent, children in self.TRACES.items() for child in children])
        artifact_df = ArtifactDataFrame([Artifact(id=self.ARTIFACT_IDS[i], content=content,
                                                  layer_id=self.LAYER_IDS[i]) for i, content in enumerate(self.ARTIFACT_CONTENT)])
        layer_df = LayerDataFrame([{LayerKeys.SOURCE_TYPE: self.PET_LAYER_ID, LayerKeys.TARGET_TYPE: self.CONCEPT_LAYER_ID},
                                   {LayerKeys.SOURCE_TYPE: self.FACTS_LAYER_ID, LayerKeys.TARGET_TYPE: self.PET_LAYER_ID}
                                   ])
        trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
        prompt_dataset = PromptDataset(trace_dataset=trace_dataset)
        return prompt_dataset
