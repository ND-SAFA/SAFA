import inspect
from copy import deepcopy
from typing import Callable, List, Union

from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.util.attr_dict import AttrDict

FINE_TUNE_REQUEST = AttrDict({
    "training_file": "training_id",
    "validation_file": "validation_id",
    "model": "gpt-3.5-turbo",
    "n_epochs": 2,
    "batch_size": 4,
    "learning_rate_multiplier": 0.05,
    "prompt_loss_weight": 0.01,
    "compute_classification_metrics": False,
    "classification_n_classes": 2,
    "classification_positive_class": " yes",
    "suffix": "custom-model-name"
})

COMPLETION_REQUEST = AttrDict({
    "model": "gpt-3.5-turbo",
    "prompt": "Say this is a test",
    "max_tokens": 7,
    "temperature": 0,
    "top_p": 1,
    "n": 1,
    "stream": False,
    "logprobs": None,
    "stop": "\n"
})

FINE_TUNE_RESPONSE_DICT = AttrDict({
    "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
    "object": "fine-tune",
    "model": "curie",
    "created_at": 1614807352,
    "events": [
        AttrDict({
            "object": "fine-tune-event",
            "created_at": 1614807352,
            "level": "info",
            "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
        })
    ],
    "fine_tuned_model": None,
    "hyperparams": AttrDict({
        "batch_size": 4,
        "learning_rate_multiplier": 0.1,
        "n_epochs": 4,
        "prompt_loss_weight": 0.1,
    }),
    "organization_id": "org-...",
    "result_files": [],
    "status": "pending",
    "validation_files": [],
    "training_files": [
        AttrDict({
            "id": "file-XGinujblHPwGLSztz8cPS8XY",
            "object": "file",
            "bytes": 1547276,
            "created_at": 1610062281,
            "filename": "my-data-train.jsonl",
            "purpose": "fine-tune-train"
        })
    ],
    "updated_at": 1614807352,
})

COMPLETION_RESPONSE_DICT = AttrDict({
    "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
    "object": "text_completion",
    "created": 1589478378,
    "model": "gpt-3.5-turbo",
    "choices": [
        AttrDict({
            "message": {
                "content": "\n\nThis is indeed a test"
            },
            "index": 0,
            "logprobs": AttrDict({"top_logprobs": [
                AttrDict({
                    " yes": -0.6815379,
                    " no": -1.0818866
                })
            ]}),

            "finish_reason": "length"
        })
    ],
    "usage": AttrDict({
        "prompt_tokens": 5,
        "completion_tokens": 7,
        "total_tokens": 12
    })})

SUMMARY_FORMAT = "Summary of {}"
DEFAULT_SUMMARY_TAG = SupportedPrompts.NL_SUMMARY.value[0].response_manager.response_tag
from unittest import mock

library_map = {
    "openai": "openai.ChatCompletion.create",
    "anthropic": "AnthropicManager.Client.completion"
}


def mock_ai(library: str, response_formatter: Callable, func=None, format: str = None, test_expected_responses: bool = True,
            *outer_args,
            **outer_kwargs):
    """
    Automatically mocks open ai
    :param format: The format to encapsulate responses in.
    :return: The decorated function with open ai mocked.
    """
    library_mock_string = library_map[library]

    def decorator(test_func: Callable, *test_func_args, **test_func_kwargs):
        @mock.patch(library_mock_string)
        def wrapper(self, mock_completion):
            response_manager = TestResponseManager(format=format, response_formatter=response_formatter, *test_func_args, *outer_args,
                                                   **test_func_kwargs, **outer_kwargs)
            mock_completion.side_effect = response_manager
            if does_accept(test_func, response_manager):
                test_func(self, response_manager)
            else:
                test_func(self)
            if test_expected_responses:
                n_used = response_manager.start_index
                n_expected = len(response_manager.responses)
                assert n_used == n_expected, f"Response manager had {n_expected - n_used} / {n_expected} unused responses."

        function_name = test_func.__name__ if hasattr(test_func, "__name__") else func.__name__
        wrapper.__name__ = function_name
        return wrapper

    return decorator


def create_openai_handler(format: str = None, *args, **kwargs):
    def handler(*handler_args, **handler_kwargs):
        def processor(t):
            if format:
                return format.format(t)
            return t

        response_text = TestResponseManager(response_formatter=processor, *args, *handler_args, **kwargs, **handler_kwargs)
        return response_text

    return handler


DEFAULT_RESPONSE = deepcopy(COMPLETION_RESPONSE_DICT["choices"][0]["message"]["content"])


class TestResponseManager:
    def __init__(self,
                 responses: Union[str, List[str]] = None,
                 tags: List[str] = None,
                 response_formatter: Callable = None,
                 format: str = None):
        if responses is None:
            responses = [DEFAULT_RESPONSE]
        if tags is None:
            tags = [DEFAULT_SUMMARY_TAG]
        self.responses = responses
        self.tags = tags
        self.response_formatter = response_formatter
        self.format = format
        self.n_given = 0
        self.start_index = 0
        self.end_index = len(responses)

    def __call__(self, *args, **kwargs) -> List[str]:
        prompts = [m["content"] for m in kwargs["messages"]]
        n_prompts = len(prompts)
        responses = self.get_next_response(n_requested=n_prompts)
        if self.response_formatter is not None:
            responses = [self.response_formatter(r) for r in responses]
        if self.format:
            responses = [self.format.format(r) for r in responses]
        self.n_given += n_prompts
        formatted_response = self.response_formatter(responses)
        return formatted_response

    def set_responses(self, responses: List[str]):
        self.responses = responses
        self.start_index = 0

    def get_next_response(self, n_requested: int = 1) -> List[str]:
        end_index = self.n_given + n_requested
        n_responses = len(self.responses)
        if end_index > n_responses:
            raise ValueError(f"Ran out of mock responses. Contains only {n_responses} responses.")
        responses = self.responses[self.start_index: end_index]
        self.start_index = end_index
        return responses


def process_response_tags(prompts: List[str], tags: List[str]):
    tag = None
    for t in tags:
        if f"<{t}>" in prompts[0]:
            tag = t
            break
    for prompt_suffix in [AnthropicManager.prompt_args.prompt_suffix, OpenAIManager.prompt_args.prompt_suffix]:
        success = False
        for p in prompts:
            if p.endswith(prompt_suffix):
                success = True
        if success:
            prompts = ["".join(p.rsplit(prompt_suffix, 1)) for p in prompts]
            break
    return prompts, tag


def does_accept(func, arg):
    """
    Check if a given function accepts a given argument.
    :param func: The function to check.
    :param arg: The argument to check if it's accepted by the function.
    :returns: True if the function accepts the argument, False otherwise.
    """
    try:
        for arg_name, arg_parameter in inspect.signature(func).parameters.items():
            if isinstance(arg, arg_parameter.annotation):
                return True
        return False
    except TypeError:
        return False
