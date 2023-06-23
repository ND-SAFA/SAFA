from typing import Any

from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType

DEFAULT_BODY_TITLE = "# Artifacts"


def builder_method(func):
    def decorator(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return decorator


class RankingPromptBuilder:
    def __init__(self, goal: str = "", query: str = "", instructions: str = "", body_title: str = DEFAULT_BODY_TITLE,
                 section_delimiter: str = "\n\n"):
        self.goal = goal
        self.query = query
        self.instructions = instructions
        self.section_delimiter = section_delimiter
        self.body_title = body_title
        self.body = ""
        self.context = ""

    @builder_method
    def with_query(self, query: str):
        self.query = query

    @builder_method
    def with_task(self, task: str):
        self.goal = task

    @builder_method
    def with_body_title(self, body_title: str):
        self.body_title = body_title

    @builder_method
    def with_format(self, format: str):
        self.instructions = format

    @builder_method
    def with_artifact(self, artifact_name: Any, artifact_body: str):
        self.body += self.format_artifact(artifact_name, artifact_body)

    @builder_method
    def with_body(self, body: str):
        self.body = body

    @builder_method
    def with_context(self, context: str):
        self.context = context

    def get(self):
        body = self.join_prompts([self.body_title, self.body], "\n\n")
        items = [self.goal + self.query, body, self.context, self.instructions]
        prompt = self.join_prompts(items, self.section_delimiter)
        return prompt

    def complete(self, llm_manager: AbstractLLMManager, **kwargs):
        params = {"temperature": 0, "prompt": self.get(), **kwargs}
        return llm_manager.make_completion_request(LLMCompletionType.GENERATION, **params)

    @staticmethod
    def format_artifact(artifact_name: str, artifact_body: str, separator: str = "\n\n"):
        body = artifact_body.replace("\n\n", "\n")
        return f"<artifact><id>{artifact_name}</id><body>{body}</body></artifact>{separator}"

    @staticmethod
    def join_prompts(prompts, delimiter):
        items = list(filter(lambda s: s is not None and len(s) > 0, prompts))
        prompt = delimiter.join(items).strip()
        return prompt
