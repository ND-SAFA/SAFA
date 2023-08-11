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
        self.handlers = []

    def __call__(self, *args, **kwargs) -> List[str]:
        prompts_global = self.get_prompts(kwargs)
        handled_responses, manual_prompts = self.run_prompt_handlers(prompts_global)

        n_manual_prompts = len(manual_prompts)
        manual_responses = self.get_next_response(n_requested=n_manual_prompts)
        manual_responses = [r(manual_prompts[i]) if callable(r) else r for i, r in enumerate(manual_responses)]
        responses = handled_responses + manual_responses
        responses = self.response_formatter(responses)
        if self.format:
            responses = [self.format.format(r) for r in responses]
        self.n_given += n_manual_prompts
        return responses

    def run_prompt_handlers(self, prompts):
        handled_responses = []
        unhandled_prompts = []
        for p in prompts:
            unhandled_prompts.append(p)
            for h in self.handlers:
                h_response = h(p)
                if h_response:
                    handled_responses.append(h_response)
                    unhandled_prompts.pop()
                    break

        return handled_responses, unhandled_prompts

    def set_responses(self, responses: List[Union[str, Callable[[str], str]]]):
        self._responses = responses
        self.start_index = 0
        self.end_index = len(responses)

    def mock_summarization(self) -> None:
        """
        Adds handler that will generically process the artifact summarization whenever it is detected.
        :return: None
        """

        def summarization_handler(p: str):
            summary_tag = "<summary>"
            if summary_tag in p:
                return self.create_summarization_response(p)
            return None

        if summarization_handler not in self.handlers:
            self.handlers.append(summarization_handler)

    def mock_responses(self):
        def response_handler(p: str):
            return "mock text"

        if response_handler not in self.handlers:
            self.handlers.append(response_handler)
        print("hi")

    @staticmethod
    def create_summarization_response(p: str):
        """
        Generically creates a summarize response from the body of the artifact.
        :param p: The summarization prompt.
        :return: The summarization response for prompt.
        """
        start_body_tag = "</summary>"
        end_body_tag = "Assistant:"
        body_start = p.find(start_body_tag)
        body_end = p.find(end_body_tag)
        artifact_body = p[body_start + len(start_body_tag): body_end].strip()
        summary = f"<summary>Summary of {artifact_body}</summary>"
        return summary

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
