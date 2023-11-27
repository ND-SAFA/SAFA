from typing import Callable, Dict, List, Union

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.util.llm_response_util import LLMResponseUtil


class TestAIManager:
    def __init__(self, library: str, response_formatter: Callable, require_used_all_responses: bool = True):
        self.library = library
        self._responses = []
        self.response_formatter = response_formatter
        self.n_used = 0
        self.start_index = 0
        self.end_index = 0
        self.handlers = []
        self.mock_calls = 0
        self.require_used_all_responses = require_used_all_responses

    def __call__(self, *args, **kwargs) -> List[str]:
        prompts_global = self.get_prompts(kwargs)
        handled_responses, manual_prompts = self.run_prompt_handlers(prompts_global)

        n_manual_prompts = len(manual_prompts)
        manual_responses = self.get_next_response(n_requested=n_manual_prompts, prompts=manual_prompts)

        self.n_used += n_manual_prompts
        self.mock_calls += n_manual_prompts

        manual_responses = [r(manual_prompts[i]) if callable(r) else r for i, r in enumerate(manual_responses)]
        responses = handled_responses + manual_responses
        responses = self.response_formatter(responses)

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

    def set_responses(self, responses: List[Union[str, Callable[[str], str]]], start_index: int = 0):
        n_responses = len(responses)
        self._responses = responses
        self.start_index = start_index
        self.end_index = n_responses

    def add_responses(self, new_responses: List[Union[str, Callable[[str], str]]]):
        """
        Adds new responses to the manager
        :param new_responses: List of new responses to add
        :return: None
        """
        self.set_responses(self._responses + new_responses, start_index=self.start_index)

    def mock_summarization(self) -> None:
        """
        Adds handler that will generically process the artifact summarization whenever it is detected.
        :return: None
        """

        def summarization_handler(p: str):
            summary_tag = "<summary>"
            if summary_tag in p:
                self.mock_calls += 1
                return self.create_summarization_response(p)
            return None

        if summarization_handler not in self.handlers:
            self.handlers.append(summarization_handler)

    def mock_responses(self):
        def response_handler(p: str):
            return "mock text"

        if response_handler not in self.handlers:
            self.handlers.append(response_handler)

    @staticmethod
    def create_summarization_response(p: str):
        """
        Generically creates a summarize response from the body of the artifact.
        :param p: The summarization prompt.
        :return: The summarization response for prompt.
        """
        start_body_tag = "</summary>"
        end_body_tag = "Assistant:"
        artifact_body = LLMResponseUtil.parse(p, "artifact", return_res_on_failure=False)
        if not artifact_body:
            artifact_body = EMPTY_STRING
            split_prompt = p.split("# Code")
            if len(split_prompt) > 1:
                artifact_body = [v for v in split_prompt[1].split("\n") if v]
        if len(artifact_body) == 0:
            body_start = p.find(start_body_tag)
            body_end = p.find(end_body_tag)
            artifact_body = p[body_start + len(start_body_tag): body_end].strip()
        else:
            artifact_body = artifact_body[0].strip()
        summary = f"<summary>Summary of {artifact_body}</summary>"
        return summary

    def get_next_response(self, n_requested: int = 1, prompts: List[str] = None) -> List[str]:
        total_requested = self.n_used + n_requested
        n_responses = len(self._responses)
        if total_requested > n_responses:
            prompts_error = f"{NEW_LINE}{NEW_LINE.join(prompts)}".strip()
            raise ValueError(f"Requested {total_requested} out of {n_responses} responses.{prompts_error}")

        responses = self._responses[self.start_index: total_requested]
        self.start_index = total_requested
        return responses

    def get_prompts(self, kwargs: Dict):
        if self.library == "openai":
            return [m["content"] for m in kwargs["messages"]]
        elif self.library == "anthropic":
            return [kwargs["prompt"]]

    def on_test_end(self) -> None:
        n_used = self.start_index
        n_expected = len(self._responses)
        if self.require_used_all_responses:
            response_txt = NEW_LINE.join(self._responses)
            assert n_used == n_expected, f"Response manager had {n_expected - n_used} / {n_expected} unused responses.{response_txt}"
