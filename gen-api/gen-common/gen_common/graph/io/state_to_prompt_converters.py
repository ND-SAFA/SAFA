from abc import abstractmethod
from typing import Any, List, Dict

from langchain_core.documents.base import Document

from gen_common.llm.prompts.context_prompt import ContextPrompt
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt

from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_args import PromptArgs


class iConverter:

    @staticmethod
    @abstractmethod
    def convert(val: Any, name: str, title: str = None) -> List[Prompt]:
        """
        Converts state variable into a prompt for the LLM.
        :param val: The state value.
        :param name: The name of the variable.
        :param title: Optional title to display for the state var (usually the name of the variable)
        :return: The prompts for display the context documents.
        """


class DocumentPromptConverter(iConverter):

    @staticmethod
    def convert(val: Dict[str, List[Document]], **kwargs) -> List[Prompt]:
        """
        Converts context documents into prompts.
        :param val: The state value containing the context documents.
        :return: The prompts for display the context documents.
        """
        context_prompts = []
        for name, documents in val.items():
            title = f"Documents related to '{name}'"
            context_prompt = ContextPromptConverter.convert(val=documents, name=name, title=title)
            context_prompts.append(context_prompt)
        return context_prompts


class ContextPromptConverter(iConverter):

    @staticmethod
    def convert(val: List[Document], name: str, title: str = None) -> Prompt:
        """
        Converts context documents into prompts.
        :param val: The state value containing the context documents.
         :param name: The name of the variable.
        :param title: Optional title to display for the state var (usually the name of the variable)
        :return: The prompts for display the context documents.
        """
        context_prompt = ContextPrompt(include_ids=True, prompt_args=PromptArgs(title=title, structure_with_new_lines=True),
                                       build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                       context_key=name)
        return context_prompt
