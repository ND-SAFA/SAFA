from typing import List, Tuple, Union

from common_resources.tools.util.attr_dict import AttrDict


def anthropic_response_formatter(responses: List[str]):
    """
    Formats the responses in the anthropic API format.
    :param responses: The responses to format.
    :return: Anthropic API response.
    """
    assert isinstance(responses, list), "Expected list as response from anthropic mock."
    assert len(responses) == 1, "Expected single response in anthropic responses."
    res = AttrDict({"content": [AttrDict({"text": responses[0]})]})
    return res


def openai_response_formatter(responses: List[Union[str, Tuple]]):
    """
    Formats the responses in the OpenAI API format.
    :param responses: The responses to format.
    :return: OpenAI API response.
    """
    assert len(responses) == 1, f"Expected responses to contain single output but got: {len(responses)}"
    r = responses[0]
    if isinstance(r, tuple):
        content, logprobs = r
        logprobs = AttrDict({"top_logprobs": [logprobs]})
    else:
        content = r
        logprobs = None

    entry = AttrDict({
        "choices": [
            AttrDict({
                "message": {
                    "content": content
                },
                "logprobs": logprobs
            })
        ],

        "id": "id"
    })
    return entry
