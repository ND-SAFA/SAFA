import uuid
from typing import Callable, Dict, List

from anthropic.types.message import Message
from anthropic.types.text_block import TextBlock
from anthropic.types.tool_use_block import ToolUseBlock
from anthropic.types.usage import Usage
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.pydantic_v1 import root_validator
from pydantic.v1.main import BaseModel

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from gen_common.graph.io.graph_state_vars import GraphStateVars
from gen_common.util.attr_dict import AttrDict
from gen_common.util.dict_util import DictUtil
from gen_common.util.reflection_util import ReflectionUtil

RESPONSE_TYPE = List[BaseModel | Callable[[str], str] | str | Exception]
MULTI_RUN_RESPONSE_TYPE = Dict[str, RESPONSE_TYPE]


class FakeClaude:
    DEFAULT_RESPONSE_ITER_ID = str(uuid.uuid4())

    def __init__(self, model: str, responses: MULTI_RUN_RESPONSE_TYPE | RESPONSE_TYPE, run_async: bool = False):
        """
        Used in place of the real claude client for testing.
        :param model: Model name of the deployment model.
        :param responses: List of responses to use for mocking.
        :param run_async: If True, generates async.
        """
        self.model = model
        if isinstance(responses, list):
            responses = {self.DEFAULT_RESPONSE_ITER_ID: responses}
        self.responses = responses
        self.response_iter = {k: iter(res) for k, res in self.responses.items()}
        self.messages = AttrDict({"create": self.get_next_response_async if run_async else self.get_next_response})

    async def get_next_response_async(self, *args, **kwargs) -> Message:
        """
        Handles get the mock response for the client when running asynchronously.
        :param args: Args to the Anthropic API.
        :param kwargs: Kwargs to the Anthropic API.
        :return: A mocked response message from fake claude.
        """
        res = self.get_next_response(*args, **kwargs)
        return res

    def get_next_response(self, *args, **kwargs) -> Message:
        """
        Handles get the mock response for the client.
        :param args: Args to the Anthropic API.
        :param kwargs: Kwargs to the Anthropic API.
        :return: A mocked response message from fake claude.
        """
        res = self._get_next_response(**kwargs)
        if ReflectionUtil.is_instance_or_subclass(res, Exception):
            raise res

        if hasattr(res, "__call__"):
            res = res(*args, **kwargs)

        if isinstance(res, BaseModel):
            content = [ToolUseBlock(id=f'toolu_{uuid.uuid4()}', input=vars(res),
                                    name=res.__class__.__name__, type='tool_use')]
            stop_reason = "end_turn"
        else:
            content = [TextBlock(text=res, type="text")]
            stop_reason = "tool_use"
        fake_msg = Message(id=f'msg_{uuid.uuid4()}', content=content, model=self.model, role='assistant',
                           stop_reason=stop_reason, stop_sequence=None, type='message',
                           usage=Usage(input_tokens=554, output_tokens=67))
        return fake_msg

    def _get_next_response(self, **kwargs) -> Callable | BaseModel | str:
        """
        Safely gets the next response for current thread.
        :param kwargs: The arguments to the model.
        :return: The mocked response.
        """
        thread_id = self._get_thread_id_from_message(**kwargs)
        assert thread_id in self.response_iter, f"No given responses for thread {thread_id}"
        response_iter = self.response_iter[thread_id]
        try:
            res = next(response_iter)
        except StopIteration:
            raise StopIteration("Not enough responses provided.")
        return res

    def _get_thread_id_from_message(self, messages: List, **kwargs) -> str:
        """
        Finds and extracts thread id from the message.
        :param messages: The messages given to the model.
        :return: The thread id.
        """
        message = messages[-1]["content"]
        thread_id_identifier = GraphStateVars.THREAD_ID.prompt_config.title
        thread_id = self.DEFAULT_RESPONSE_ITER_ID
        if thread_id_identifier in message:
            thread_id_subset = message.split(thread_id_identifier)[-1]
            end_index = thread_id_subset.find(NEW_LINE, 1)
            thread_id = thread_id_subset[1:end_index]
            if isinstance(thread_id, list):
                thread_id = EMPTY_STRING.join(thread_id)
        return thread_id


class TestChatModel(ChatAnthropic):
    responses: RESPONSE_TYPE | MULTI_RUN_RESPONSE_TYPE

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """
        Overwrites the client to use fake claude.
        :param values: The input values to the model.
        :return: The updated values.
        """
        values = super().validate_environment(values)
        values["_client"] = FakeClaude(values["model"], values["responses"])
        values["_async_client"] = FakeClaude(values["model"], values["responses"], run_async=True)
        return values


class TestResponseManager:

    def __init__(self):
        """
        Manages the fake model and the expected responses.

        """
        self.__model = None
        self._responses = []

    def __call__(self, *args, **kwargs):
        """
        Initializes the fake model.
        :param args: Args to the model.
        :param kwargs: Kwargs to the model.
        :return: The model.
        """
        if not self.__model:
            kwargs = DictUtil.update_kwarg_values(kwargs, responses=self._responses)
            self.__model = TestChatModel(**kwargs)
        return self.__model

    def set_responses(self, responses: RESPONSE_TYPE | MULTI_RUN_RESPONSE_TYPE, start_index: int = 0):
        """
        Sets the fake responses for the model.
        :param responses: The fake responses for the model.
        :param start_index: The starting index of the next response.
        :return: None
        """
        self._responses = responses
