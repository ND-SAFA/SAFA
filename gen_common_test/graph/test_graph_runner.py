from unittest import TestCase

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import LayerKeys, TraceKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.graph.branches.supported_branches import SupportedBranches
from gen_common.graph.edge import Edge
from gen_common.graph.graph_definition import GraphDefinition
from gen_common.graph.graph_runner import GraphRunner
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.llm_tools.tool_models import ExploreArtifactNeighborhood, RequestAssistance, RetrieveAdditionalInformation
from gen_common.graph.nodes.generate_node import AnswerUser, GenerateNode
from gen_common.graph.nodes.supported_nodes import SupportedNodes
from gen_common_test.base.mock.decorators.chat import mock_chat_model
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager


class TestGraphRunner(TestCase):
    CONCEPT_LAYER_ID = "concepts"
    PET_LAYER_ID = "pets"
    FACTS_LAYER_ID = "facts"
    ARTIFACT_CONTENT = ["dogs", "cats",  # 0, 1
                        "Cat1: Michael", "Dog1: Scruffy", "Cat2: Meredith", "Dog2: Rocky",  # 2, 3, 4, 5
                        "Michael is quite fat", "Meredith bites a lot", "Rocky loves bubbles", "Scruffy has a toupee",  # 6, 7, 8, 9
                        "Cats are better than dogs"]  # 10
    ARTIFACT_IDS = [f"{i}" for i, _ in enumerate(ARTIFACT_CONTENT)]
    LAYER_IDS = [CONCEPT_LAYER_ID] * 2 + [PET_LAYER_ID] * 4 + [FACTS_LAYER_ID] * 5
    TRACES = {
        0: [3, 5, 10],
        1: [2, 4, 10],
        2: [6],
        3: [9],
        4: [7],
        5: [8],
    }
    QUESTION = "What pet should I get?"
    ANSWER = "Michael seems like the best option since cats are better than dogs and meredith bites a lot which is less preferable."
    REFERENCE_IDS = ["6", "7", "2", "10"]

    @mock_chat_model
    def test_full_generation(self, response_manager: TestResponseManager):
        first_res = RetrieveAdditionalInformation(retrieval_query="best pet")
        second_res = ExploreArtifactNeighborhood(artifact_ids=1, artifact_types="pets")
        third_res = ExploreArtifactNeighborhood(artifact_ids=[2, 4])
        repeat_res = RetrieveAdditionalInformation(retrieval_query="best pet")
        final_res = GenerateNode(self.get_args()).get_agent().create_response_obj([self.ANSWER, self.REFERENCE_IDS])
        response_manager.set_responses([first_res, second_res, third_res, repeat_res, final_res])
        answer_obj, runner = self.run_chat_test(response_manager)
        self.assertIsInstance(answer_obj, AnswerUser)
        self.assertEqual(answer_obj.answer, self.ANSWER)
        self.assertListEqual(answer_obj.reference_ids, self.REFERENCE_IDS)

        generate_node = SupportedNodes.GENERATE.name
        retrieve_node = SupportedNodes.RETRIEVE.name
        explore_node = SupportedNodes.EXPLORE_NEIGHBORS.name
        continue_node = SupportedNodes.CONTINUE.name
        self.assertListEqual(runner.get_nodes_visited_on_last_run(),
                             [generate_node, retrieve_node, generate_node, explore_node,
                              generate_node, explore_node, generate_node,
                              generate_node, continue_node])
        self.assertEqual(runner.get_states_from_last_run()[-1]['generation'], self.ANSWER)
        runner.clear_run_history()
        self.assertIsNone(runner.get_nodes_visited_on_last_run())
        self.assertIsNone(runner.get_states_from_last_run())

    @mock_chat_model
    def test_with_request_assistance(self, response_manager: TestResponseManager):
        first_res = RetrieveAdditionalInformation(retrieval_query="best pet")
        second_res = ExploreArtifactNeighborhood(artifact_ids=1, artifact_types="pets")
        response_manager.set_responses([first_res, second_res, first_res, second_res, "I dont know"])
        answer_obj, runner = self.run_chat_test(response_manager)
        self.assertIsNone(answer_obj)

    @mock_chat_model
    def test_with_failure(self, response_manager: TestResponseManager):
        first_res = RetrieveAdditionalInformation(retrieval_query="best pet")
        final_res = RequestAssistance()
        response_manager.set_responses([first_res, final_res])
        answer_obj, runner = self.run_chat_test(response_manager)
        self.assertIsInstance(answer_obj, RequestAssistance)
        self.assertEqual(answer_obj.relevant_information_learned, final_res.relevant_information_learned)
        self.assertEqual(answer_obj.related_doc_ids, final_res.related_doc_ids)

    def run_chat_test(self, response_manager: TestResponseManager):
        args = self.get_args()
        runner = GraphRunner(self.get_definition())
        answer_obj = runner.run(args)
        return answer_obj, runner

    def get_definition(self):
        return GraphDefinition(
            nodes=[
                SupportedNodes.GENERATE,
                SupportedNodes.RETRIEVE,
                SupportedNodes.CONTINUE,
                SupportedNodes.EXPLORE_NEIGHBORS
            ],
            edges=[
                Edge(SupportedNodes.GENERATE, SupportedBranches.DECIDE_NEXT),
                Edge(SupportedNodes.CONTINUE, SupportedNodes.END_COMMAND),
                Edge(SupportedNodes.RETRIEVE, SupportedNodes.GENERATE),
                Edge(SupportedNodes.EXPLORE_NEIGHBORS, SupportedNodes.GENERATE)],
            state_type=GraphState)

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

    def get_args(self):
        args = GraphArgs(user_question=self.QUESTION, dataset=self.construct_dataset())
        return args
