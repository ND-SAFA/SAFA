from copy import deepcopy
from typing import Any, Callable, Dict, List, Union

from tgen.common.constants.deliminator_constants import COLON, EMPTY_STRING, NEW_LINE
from tgen.common.constants.project_summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS, PROJECT_SUMMARY_TAGS, PS_DATA_FLOW_TAG, \
    PS_ENTITIES_TAG, PS_SUBSYSTEM_TAG
from tgen.common.constants.ranking_constants import CHANGE_IMPACT_TAG, DERIVATION_TAG, ENTITIES_TAG, JUSTIFICATION_TAG, \
    RANKING_ARTIFACT_TAG, RANKING_EXPLANATION_TAG, RANKING_ID_TAG, RANKING_SCORE_TAG, SUB_SYSTEMS_TAG
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.core.args.anthropic_args import AnthropicParams

DEFAULT_SCORE = 0.5
DEFAULT_EXPLANATION = "EXPLANATION"
SUMMARY_TAGS = {"summary", "descrip"}


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
        prompts_global, system_prompt = self.get_prompts(kwargs)
        handled_responses, manual_prompts = self.run_prompt_handlers(prompts_global)

        n_manual_prompts = len(manual_prompts)
        manual_responses = self.get_next_response(n_requested=n_manual_prompts, prompts=manual_prompts)

        self.n_used += n_manual_prompts
        self.mock_calls += n_manual_prompts

        inputs4callables = [(manual_prompts[i], system_prompt) if system_prompt else manual_prompts[i]
                            for i, r in enumerate(manual_responses)]
        manual_responses = [r(inputs4callables[i]) if callable(r) else r for i, r in enumerate(manual_responses)]
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

    def mock_ranking(self, artifact_ids: List[Any], scores: List[float] = None,
                     explanations: List[str] = None, default_score: float = DEFAULT_SCORE,
                     default_explanation: str = DEFAULT_EXPLANATION):
        """

        :param artifact_ids: Artifacts being ranked.
        :param scores: The score to assign to each artifact.
        :param explanations: The explanations to assign to each artifact item.
        :param default_score: The default score to use.
        :param default_explanation: The default explanation to use.
        :return: None, responses added in place.
        """
        n_artifacts = len(artifact_ids)
        if scores is None:
            scores = [default_score] * n_artifacts

        if all(isinstance(f, float) for f in scores):
            scores = [round(s * 5) for s in scores]
        if explanations is None:
            explanations = [default_explanation] * n_artifacts

        responses = []
        for artifact_id, score, explanation in zip(artifact_ids, scores, explanations):
            tag2response = {
                RANKING_ID_TAG: artifact_id,
                RANKING_EXPLANATION_TAG: explanation,
                RANKING_SCORE_TAG: score
            }
            explanation_content = self.create_response_content(tag2response)
            responses.append(PromptUtil.create_xml(RANKING_ARTIFACT_TAG, tag_content=explanation_content))
        response = NEW_LINE.join(responses)
        self.add_responses([response])

    def mock_explanations(self, n_explanations: int, scores: List[float] = None, default_score: float = 0.5) -> None:
        if scores is None:
            scores = [default_score] * n_explanations
        tag2response = {
            SUB_SYSTEMS_TAG: "SUB_SYSTEM",
            ENTITIES_TAG: "ENTITIES",
            DERIVATION_TAG: "DERIVATION",
            CHANGE_IMPACT_TAG: "IMPACT",
            JUSTIFICATION_TAG: "JUSTIFICATION"
        }
        responses = []
        assert n_explanations == len(scores), f"Expected ({n_explanations}) scores but got {scores}"

        for score in scores:
            tag2response[RANKING_SCORE_TAG] = score
            response = self.create_response_content(tag2response)
            responses.append(response)
        self.add_responses(responses)

    def add_xml_response(self, xml_map: Dict, as_single_res: bool = False, delimiter: str = NEW_LINE):
        """
        Adds responses where keys are xml keys and the body of those keys is the body of the xml tags.
        :param xml_map: The map containing key and content to use.
        :param as_single_res: Whether to combine the responses into a single response.
        :param delimiter: The delimiter used to insert between each response if as_single_res is true.
        :return: None
        """
        responses = []
        for tag, res in xml_map.items():
            r_children = [res] if isinstance(res, str) else [r for r in res]
            responses.extend([PromptUtil.create_xml(tag, r) for r in r_children])

        if as_single_res:
            responses = [delimiter.join(responses)]

        self.add_responses(responses)

    def mock_summarization(self, responses: List[str] = None) -> None:
        """
        Adds handler that will generically process the artifact summarization whenever it is detected.
        :return: None
        """

        if responses:
            new_responses = [PromptUtil.create_xml("summary", r) for r in responses]
            self.add_responses(new_responses)
            return

        def summarization_handler(p: str):
            for tag in SUMMARY_TAGS:
                if PromptUtil.create_xml_opening(tag) in p:
                    self.mock_calls += 1
                    return self.create_summarization_response(p, tag_name=tag)
            return None

        if summarization_handler not in self.handlers:
            self.handlers.append(summarization_handler)

    def mock_project_summary(self, sections: Dict[str, str]):
        responses = [self.create_project_summary_response(PROJECT_SUMMARY_TAGS[s], sections[s])
                     for s in DEFAULT_PROJECT_SUMMARY_SECTIONS]
        self.add_responses(responses)
        return responses

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
            return [m["content"] for m in kwargs["messages"]], None
        elif self.library == "anthropic":
            return [EMPTY_STRING.join([m["content"] for m in kwargs[AnthropicParams.MESSAGES]])], kwargs.get(AnthropicParams.SYSTEM)

    def on_test_end(self) -> None:
        n_used = self.start_index
        n_expected = len(self._responses)
        if self.require_used_all_responses:
            response_txt = NEW_LINE.join([str(r) for r in self._responses])
            assert n_used == n_expected, f"Response manager had {n_expected - n_used} / {n_expected} unused responses.{response_txt}"

    @staticmethod
    def create_response_content(tag2response: Dict, multi_tags: List[str] = None) -> str:
        """
        Creates a response containing the keys as tags and values as their contents.
        :param tag2response: Tags and their
        :param multi_tags:
        :return:
        """
        if multi_tags is None:
            multi_tags = []
        response = EMPTY_STRING
        if multi_tags:
            tags = []
            for mt in multi_tags:
                for st in tag2response[mt]:
                    copy_tag = deepcopy(tag2response)
                    copy_tag[mt] = st  # override multi-tag with single tag
                    tags.append(copy_tag)
        else:
            tags = [tag2response]
        for t in tags:
            response += NEW_LINE.join(PromptUtil.create_xml(t, r) for t, r in t.items())
        return response

    @staticmethod
    def validate_inputs(*items) -> None:
        """
        Verifies that lists all have same length.
        :param items; Positional arguments of lists to verify.
        :return: None, verifications in place.
        """
        n_items = len(items[0])
        for item in items[1:]:
            assert len(item) == n_items, f"Expected {item} to have {n_items} elements."

    @staticmethod
    def create_project_summary_response(tag: str, tag_body: Union[str, Dict]):
        NAMED_RESPONSE_TAGS = [PS_SUBSYSTEM_TAG, PS_ENTITIES_TAG]
        if isinstance(tag_body, dict):
            chunks = tag_body["chunks"]
            if tag in NAMED_RESPONSE_TAGS:
                body = [TestAIManager.create_named_response(tag, c) for c in chunks]
            elif tag == PS_DATA_FLOW_TAG:
                body = PromptUtil.create_xml(tag, NEW_LINE.join(chunks))
            else:
                body = [PromptUtil.create_xml(tag, c) for c in chunks]
        else:
            if tag in NAMED_RESPONSE_TAGS:
                tag_body = TestAIManager.create_named_response(tag, tag_body)
            body = f"<{tag}>{tag_body}</{tag}>"
        return f"<notes></notes>{body}" if isinstance(body, str) else NEW_LINE.join([f"<notes></notes>{b}" for b in body])

    @staticmethod
    def create_named_response(tag_id: str, content: str) -> str:
        """
        Creates subsystem project summary response that contains given content.
        First line is used to name the subsystem. If no newline if found then content is used as name.
        :param tag_id: The tag to encapsulate named responsed.
        :param content: The content of the sub-system.
        :return:The response with XML tags.
        """
        delimiter = TestAIManager.find_first(content, [NEW_LINE, COLON])
        name, desc = content.split(delimiter) if delimiter else [content, content]
        name = name.strip()
        desc = desc.strip()
        name = name.replace("#", EMPTY_STRING)
        content = f"<name>{name}</name><descr>{desc}</descr>"
        content = PromptUtil.create_xml(tag_id, content)
        return content

    @staticmethod
    def find_first(content: str, items: List[str]) -> str:
        """
        Finds first item that's within content.
        :param content: The text to search within.
        :param items: The items to check one by one if they are in content.
        :return item found.
        """
        for i in items:
            if i in content:
                return i
        return None

    @staticmethod
    def mock_responses(self):
        def response_handler(p: str):
            return "mock text"

        if response_handler not in self.handlers:
            self.handlers.append(response_handler)

    @staticmethod
    def create_summarization_response(p: str, tag_name: str = "summary"):
        """
        Generically creates a summarize response from the body of the artifact.
        :param p: The summarization prompt.
        :param tag_name: The summary tag name.
        :return: The summarization response for prompt.
        """
        start_body_tag = PromptUtil.create_xml_closing(tag_name)
        end_body_tag = "Assistant:"
        artifact_body = LLMResponseUtil.parse(p, "artifact", return_res_on_failure=False)
        if not artifact_body:
            artifact_body = EMPTY_STRING
            split_prompt = p.split("# Code")
            if len(split_prompt) > 1:
                artifact_body = [[v for v in split_prompt[1].split("\n") if v][1]]
        if len(artifact_body) == 0:
            body_start = p.find(start_body_tag)
            body_end = p.find(end_body_tag)
            artifact_body = p[body_start + len(start_body_tag): body_end].strip()
        else:
            artifact_body = artifact_body[0].strip()
        summary = PromptUtil.create_xml(tag_name, f"Summary of {artifact_body}")
        return summary
