from typing import List

from pydantic.v1.fields import Field
from pydantic.v1.main import BaseModel

from common_resources.graph.agents.base_agent import BaseAgent
from common_resources.graph.io.state_var import StateVar
from common_resources.graph.branches.paths.path import Path
from common_resources.graph.branches.paths.path_selector import PathSelector
from common_resources.graph.io.graph_state_vars import GraphStateVars
from common_resources.llm.response_managers.json_response_manager import JSONResponseManager
from common_resources.mocking.langchain.mock_chat_model_decorator import mock_chat_model
from common_resources.mocking.langchain.prompt_assertion import PromptAssertion, AssertInPrompt, AssertToolAvailable
from common_resources.mocking.langchain.test_chat_model import TestResponseManager
from common_resources.tools.util.dict_util import DictUtil
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.graph.graph_test_util import PetData


class FakeResponseModel(BaseModel):
    fav_pet: str = Field(description="Your favorite pet")
    curr_pet_status: str = Field(description="Whether you currently have a pet", default="no pets")


class RequestVote(BaseModel):
    """
    Allows LLM to have others vote on their favorite pets.
    """
    vote_options: List[str] = Field(description="A list of options to vote on.")


class TestBaseAgent(BaseTest):
    SYSTEM_PROMPT = "Whats your favorite pet?"
    RESPONSE = FakeResponseModel(fav_pet="dog")

    @mock_chat_model
    def test_respond(self, test_response_manager: TestResponseManager):
        context_docs = DictUtil.get_value_by_index(PetData.get_context_docs())
        test_response_manager.set_responses([PromptAssertion([self.system_prompt_assertion]
                                                             + [AssertInPrompt(self, message_number=-1, value=doc.metadata["id"])
                                                                for doc in context_docs],
                                                             response=self.RESPONSE)]
                                            )
        agent = self.get_agent()
        args, state = PetData.get_io(include_documents=True)
        res = agent.respond(state)
        self.assert_response(res)

        try:
            args, state = PetData.get_io(most_common_pet="dog")
            res = agent.respond(state)
            self.fail("Missing key document should result in assertion error")
        except AssertionError:
            pass

    @mock_chat_model
    def test_respond_with_tools(self, test_response_manager: TestResponseManager):
        alternative_prompt = "What is your favorite food?"
        tool_response = RequestVote(vote_options=["cat", "dog", "turtle"])
        test_response_manager.set_responses([PromptAssertion([
            AssertToolAvailable(self, RequestVote),
            AssertInPrompt(self, alternative_prompt, in_system_prompt=True)
        ], tool_response)])
        llm_does_like_animals = StateVar("generation") == "I don't like animals"
        system_prompt = PathSelector(Path(condition=llm_does_like_animals,
                                          action=alternative_prompt),
                                     Path(action=self.SYSTEM_PROMPT))
        tools = PathSelector(Path(condition=llm_does_like_animals,
                                  action=[RequestVote]),
                             Path(action=[]))
        agent = self.get_agent(system_prompt=system_prompt, tools=tools)
        args, state = PetData.get_io(include_documents=True,
                                     generation="I don't like animals")
        res = agent.respond(state)
        self.assert_response(res, tool_response)

    def test_extract_response(self):
        agent = self.get_agent()
        answer = agent.extract_answer(self.RESPONSE)
        self.assertEqual(answer, self.RESPONSE.fav_pet)

    def test_create_response_obj(self):
        agent = self.get_agent()
        res_obj = agent.create_response_obj(response=self.RESPONSE.fav_pet)
        self.assertEqual(res_obj.fav_pet, self.RESPONSE.fav_pet)
        pet_status = "Have 2 dogs"
        res_obj = agent.create_response_obj(response=[self.RESPONSE.fav_pet, pet_status])
        self.assertEqual(res_obj.fav_pet, self.RESPONSE.fav_pet)
        self.assertEqual(res_obj.curr_pet_status, pet_status)

    def test_get_first_response_tag(self):
        agent = self.get_agent()
        self.assertEqual(agent.get_first_response_tag(), "fav_pet")

    def test_requires_context_prompt(self):
        self.assertTrue(BaseAgent._requires_context_prompt(PetData.get_context_docs()))

    def assert_response(self, res: BaseModel, response_model: BaseModel = RESPONSE):
        for key, value in vars(response_model).items():
            self.assertEqual(getattr(res, key), value)

    @property
    def system_prompt_assertion(self):
        system_prompt_assertion = AssertInPrompt(self, in_system_prompt=True, value=self.SYSTEM_PROMPT)
        return system_prompt_assertion

    def get_agent(self, system_prompt=SYSTEM_PROMPT, tools=None):
        response_manager = JSONResponseManager.from_langgraph_model(FakeResponseModel)
        return BaseAgent(system_prompt, response_manager, state_vars_for_context=[GraphStateVars.DOCUMENTS, GraphStateVars.GENERATION],
                         allowed_missing_state_vars={GraphStateVars.GENERATION.var_name},
                         tools=tools,
                         )
