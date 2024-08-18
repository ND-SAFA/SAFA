from langchain_core.documents.base import Document

from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.llm_tools.tool_models import ExploreArtifactNeighborhood, RequestAssistance, RetrieveAdditionalInformation, \
    STOP_TOOL_USE
from gen_common.graph.nodes.generate_node import AnswerUser, GenerateNode
from gen_common.llm.abstract_llm_manager import PromptRoles
from gen_common_test.base.mock.decorators.mock_chat_model import mock_chat_model
from gen_common_test.base.mock.langchain.prompt_assertion import AssertInPrompt, AssertToolAvailable, PromptAssertion
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.graph.graph_test_util import PetData


class TestGenerationNode(BaseTest):
    QUESTION = "What pet should I get?"
    RETRIEVE_TOOL = RetrieveAdditionalInformation(retrieval_query="best pet")
    EXPLORE_NEIGHBORHOOD_TOOL = ExploreArtifactNeighborhood(artifact_ids={"a_0"})

    ANSWER_USER_TOOL = AnswerUser(answer="You should get a cat!", reference_ids={"a_4"})
    REQUEST_ASSISTANCE_TOOL = RequestAssistance(relevant_information_learned="I learned some stuff",
                                                related_doc_ids=["a_0"])

    @mock_chat_model
    def test_request_context(self, response_manager: TestResponseManager):
        # Tests requesting context when no context is currently provided
        response_manager.set_responses([PromptAssertion([self.assert_no_context_prompt,
                                                         AssertToolAvailable(self,
                                                                             tool=RetrieveAdditionalInformation)],
                                                        self.RETRIEVE_TOOL)])
        args, state = self.get_io()
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("retrieval_query").pop(), self.RETRIEVE_TOOL.retrieval_query)

    @mock_chat_model
    def test_request_context_second_time(self, response_manager: TestResponseManager):
        # Since the exact retrieval query was already used, the tool will be stopped for future use
        # to prevent the LLM from going in a circle
        response_manager.set_responses([PromptAssertion([self.assert_context_prompt,
                                                         AssertToolAvailable(self,
                                                                             tool=RetrieveAdditionalInformation),
                                                         AssertToolAvailable(self,
                                                                             tool=ExploreArtifactNeighborhood,
                                                                             is_expected_to_be_available=False)
                                                         ],
                                                        self.RETRIEVE_TOOL)])

        args, state = self.get_io(include_documents=True,
                                  retrieval_query=self.RETRIEVE_TOOL.retrieval_query,
                                  selected_artifact_ids=STOP_TOOL_USE)
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("retrieval_query"), STOP_TOOL_USE)

    @mock_chat_model
    def test_generate(self, response_manager: TestResponseManager):
        # Tests both generation and disabling both of the other tools
        response_manager.set_responses([PromptAssertion([self.assert_context_prompt,
                                                         AssertToolAvailable(self,
                                                                             tool=ExploreArtifactNeighborhood,
                                                                             is_expected_to_be_available=False),
                                                         AssertToolAvailable(self,
                                                                             tool=RetrieveAdditionalInformation,
                                                                             is_expected_to_be_available=False)
                                                         ],
                                                        self.ANSWER_USER_TOOL)])
        args, state = self.get_io(include_documents=True,
                                  retrieval_query=STOP_TOOL_USE,
                                  selected_artifact_ids=STOP_TOOL_USE)
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("generation"), self.ANSWER_USER_TOOL.answer)
        self.assertEqual(res.get("reference_ids"), self.ANSWER_USER_TOOL.reference_ids)
        self.assertIn(self.ANSWER_USER_TOOL.__class__.__name__, res.get("tools_already_used")[0])

    @mock_chat_model
    def test_request_assistance(self, response_manager: TestResponseManager):
        # Tests both generation and disabling both of the other tools
        response_manager.set_responses([self.REQUEST_ASSISTANCE_TOOL])
        args, state = self.get_io(include_documents=True)
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("relevant_information_learned"), self.REQUEST_ASSISTANCE_TOOL.relevant_information_learned)
        self.assertEqual(res.get("related_doc_ids"), self.REQUEST_ASSISTANCE_TOOL.related_doc_ids)

    @mock_chat_model
    def test_generate_with_conversation_history_and_question_artifacts(self, response_manager: TestResponseManager):
        # Tests both generation with no reference ids and disabling of Retrieve Additional Information bc no traces

        chat_history = [(PromptRoles.USER, "This is my first question."), (PromptRoles.AI, "This is my answer to that question.")]
        artifacts_referenced_in_question = "a_0"
        tool = AnswerUser(answer=self.ANSWER_USER_TOOL.answer)
        args, state = self.get_io(include_documents=True, chat_history=chat_history,
                                  artifacts_referenced_in_question=[artifacts_referenced_in_question])

        content_referenced_in_question = args.dataset.artifact_df.get_artifact(artifacts_referenced_in_question)[ArtifactKeys.CONTENT]
        response_manager.set_responses([PromptAssertion([self.assert_context_prompt,
                                                         AssertToolAvailable(self,
                                                                             tool=ExploreArtifactNeighborhood,
                                                                             is_expected_to_be_available=False
                                                                             ),
                                                         AssertToolAvailable(self,
                                                                             tool=RetrieveAdditionalInformation),
                                                         AssertInPrompt(self, message_number=0, value=chat_history[0][1]),
                                                         AssertInPrompt(self, message_number=1, value=chat_history[1][1]),
                                                         AssertInPrompt(self, message_number=-1, value=content_referenced_in_question)
                                                         ],

                                                        tool)])

        args.dataset.trace_dataset = None  # remove traces
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("generation"), self.ANSWER_USER_TOOL.answer)
        self.assertEqual(len(res.get("reference_ids")), 0)

    @mock_chat_model
    def test_request_neighborhood(self, response_manager: TestResponseManager):
        # Tests the model requesting a neighborhood as well as both tools being available
        response_manager.set_responses([PromptAssertion([self.assert_context_prompt,
                                                         AssertToolAvailable(self,
                                                                             tool=ExploreArtifactNeighborhood),
                                                         AssertToolAvailable(self,
                                                                             tool=RetrieveAdditionalInformation)
                                                         ],
                                                        self.EXPLORE_NEIGHBORHOOD_TOOL)])
        args, state = self.get_io(include_documents=True)
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("selected_artifact_ids"), self.EXPLORE_NEIGHBORHOOD_TOOL.artifact_ids)

    @mock_chat_model
    def test_request_neighborhood_second_time(self, response_manager: TestResponseManager):
        # Since the exact artifact id was already used, the tool will be stopped for future use
        # to prevent the LLM from going in a circle
        response_manager.set_responses([PromptAssertion([self.assert_context_prompt,
                                                         AssertToolAvailable(self,
                                                                             tool=ExploreArtifactNeighborhood),
                                                         AssertToolAvailable(self,
                                                                             tool=RetrieveAdditionalInformation,
                                                                             is_expected_to_be_available=False)
                                                         ],
                                                        self.EXPLORE_NEIGHBORHOOD_TOOL)])
        docs = PetData.get_context_docs()
        docs[list(self.EXPLORE_NEIGHBORHOOD_TOOL.artifact_ids)[0]] = [Document("Neighbor of A0", metadata={"id": "neighor_0"})]
        args, state = self.get_io(documents=docs,
                                  retrieval_query=STOP_TOOL_USE,
                                  current_tools_used=[f"1. {repr(self.RETRIEVE_TOOL)}"])
        res: GraphState = GenerateNode(args).perform_action(state)
        self.assertEqual(res.get("selected_artifact_ids"), STOP_TOOL_USE)

    def assert_no_context_prompt(self, *args, **kwargs):
        # assert prompt is correct when it does not contain context
        AssertToolAvailable(self, tool=ExploreArtifactNeighborhood, is_expected_to_be_available=False)(*args, **kwargs)
        AssertToolAvailable(self, tool=AnswerUser)(*args, **kwargs)
        self.assertNotIn(GenerateNode.CONTEXT_ADDITION, kwargs.get("system"))
        message = kwargs.get("messages")[0]["content"]
        self.assertNotIn("Documents", message)

    def assert_context_prompt(self, *args, **kwargs):
        # assert prompt is correct when it does contain context
        AssertToolAvailable(self, tool=AnswerUser)(*args, **kwargs)
        self.assertIn(GenerateNode.CONTEXT_ADDITION, kwargs.get("system"))
        message = kwargs.get("messages")[-1]["content"]
        for index in PetData.CONTEXT_ARTIFACTS:
            self.assertIn(PetData.ARTIFACT_CONTENT[index], message)

    def get_io(self, **kwargs):
        return PetData.get_io(user_question=self.QUESTION,
                              **kwargs)
