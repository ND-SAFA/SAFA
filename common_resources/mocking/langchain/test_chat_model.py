import uuid
from typing import Dict, List, Callable

from anthropic.types.message import Message
from anthropic.types.text_block import TextBlock
from anthropic.types.tool_use_block import ToolUseBlock
from anthropic.types.usage import Usage
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.pydantic_v1 import root_validator
from pydantic.v1.main import BaseModel

from common_resources.tools.util.attr_dict import AttrDict
from common_resources.tools.util.dict_util import DictUtil

RESPONSE_TYPE = List[BaseModel | Callable[[str], str] | str]


class FakeClaude:

    def __init__(self, model: str, responses: RESPONSE_TYPE):
        """
        Used in place of the real claude client for testing.
        :param model: Model name of the deployment model.
        :param responses: List of responses to use for mocking.
        """
        self.model = model
        self.responses = responses
        self.response_iter = iter(self.responses)
        self.messages = AttrDict({"create": self.get_next_response})

    def get_next_response(self, *args, **kwargs) -> Message:
        """
        Handles get the mock response for the client.
        :param args: Args to the Anthropic API.
        :param kwargs: Kwargs to the Anthropic API.
        :return: A mocked response message from fake claude.
        """
        res = next(self.response_iter)
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


class TestChatModel(ChatAnthropic):
    responses: RESPONSE_TYPE

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """
        Overwrites the client to use fake claude.
        :param values: The input values to the model.
        :return: The updated values.
        """
        values = super().validate_environment(values)
        fake_claude = FakeClaude(values["model"], values["responses"])
        values["_client"] = fake_claude
        values["_async_client"] = fake_claude
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

    def set_responses(self, responses: RESPONSE_TYPE, start_index: int = 0):
        """
        Sets the fake responses for the model.
        :param responses: The fake responses for the model.
        :param start_index: The starting index of the next response.
        :return: None
        """
        self._responses = responses
