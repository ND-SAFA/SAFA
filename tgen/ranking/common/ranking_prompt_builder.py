from typing import Any, List, Optional

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.constants.tgen_constants import DEFAULT_QUERY_TAG

DEFAULT_BODY_TITLE = "# Software Artifacts"


def builder_method(func):
    """
    Decorator for builder pattern.
    :param func: The function being decorated.
    :return: Decorator return self by default.
    """

    def decorator(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return decorator


class RankingPromptBuilder:

    def __init__(self, goal: str = "", query: str = "", instructions: str = "",
                 body_title: str = DEFAULT_BODY_TITLE, section_delimiter: str = "\n\n\n", query_tag: str = DEFAULT_QUERY_TAG):
        """
        Builder for prompts with tasks.
        """
        self.goal = goal
        self.query = query
        self.instructions = instructions
        self.section_delimiter = section_delimiter
        self.body_title = body_title
        self.body = ""
        self.context = ""
        self.query_tag = query_tag

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
    def with_artifact(self, artifact_name: Any, artifact_body: str, **kwargs):
        self.body += self.format_artifact(artifact_name, artifact_body, **kwargs)

    @builder_method
    def with_body(self, body: str):
        self.body = body

    @builder_method
    def with_context(self, context: str):
        self.context = context

    def get(self):
        """
        :return: Builds and returns prompt.
        """
        query_formatted = f"<{self.query_tag}>\n{self.query}\n</{self.query_tag}>" if self.query else self.query
        body = self.join_prompts([self.body_title, self.body], "\n\n")
        items = [self.goal + query_formatted, self.context, body, self.instructions]
        prompt = self.join_prompts(items, self.section_delimiter)
        return prompt

    @staticmethod
    def format_artifact(artifact_name: str, artifact_body: str, separator: str = "\n\n", name: str = None):
        """
        Formats the artifact as xml.
        :param artifact_name: The artifact id.
        :param artifact_body: The artifact content.
        :param separator: The separator between artifacts.
        :return: Artifact prompt string.
        """
        if name:
            artifact_body = f"({name}) {artifact_body}"
        body = artifact_body.replace(f"{NEW_LINE}{NEW_LINE}", f"{NEW_LINE}")
        return f"<artifact>\n\t<id>{artifact_name}</id>\n\t<body>{body}</body>\n</artifact>{separator}"

    @staticmethod
    def join_prompts(prompts: List[Optional[str]], delimiter: str):
        """
        Joins set of optional prompts together.
        :param prompts: The prompts that may or may not exist.
        :param delimiter: The delimiter to join them with.
        :return: The joined prompt.
        """
        items = list(filter(lambda s: s is not None and len(s) > 0, prompts))
        prompt = delimiter.join(items).strip()
        return prompt
