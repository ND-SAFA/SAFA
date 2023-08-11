from typing import Callable, Dict, List, Union

from tgen.testres.testprojects.mocking.test_open_ai_responses import DEFAULT_SUMMARY_TAG


class TestAIManager:
    def __init__(self,
                 library: str,
                 response_formatter: Callable,
                 responses: Union[str, List[str]] = None,
                 tags: List[str] = None,
                 format: str = None):
        if responses is None:
            responses = []
        if tags is None:
            tags = [DEFAULT_SUMMARY_TAG]
        self.library = library
        self._responses = responses
        self.tags = tags
        self.response_formatter = response_formatter
        self.format = format
        self.n_given = 0
        self.start_index = 0
        self.end_index = len(responses)

    def __call__(self, *args, **kwargs) -> List[str]:
        prompts = self.get_prompts(kwargs)
        n_prompts = len(prompts)
        responses = self.get_next_response(n_requested=n_prompts)
        responses = [r(prompts[i]) if callable(r) else r for i, r in enumerate(responses)]
        responses = self.response_formatter(responses)
        if self.format:
            responses = [self.format.format(r) for r in responses]
        self.n_given += n_prompts
        return responses

    def set_responses(self, responses: List[Union[str, Callable[[str], str]]]):
        self._responses = responses
        self.start_index = 0
        self.end_index = len(responses)

    def get_next_response(self, n_requested: int = 1) -> List[str]:
        end_index = self.n_given + n_requested
        n_responses = len(self._responses)
        if end_index > n_responses:
            raise ValueError(f"Ran out of mock responses. Contains only {n_responses} responses.")

        responses = self._responses[self.start_index: end_index]
        self.start_index = end_index
        return responses

    def get_prompts(self, kwargs: Dict):
        if self.library == "openai":
            return [m["content"] for m in kwargs["messages"]]
        elif self.library == "anthropic":
            return [kwargs["prompt"]]
