from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Set

from tgen.chat.message_meta import MessageMeta
from tgen.common.util.dataclass_util import required_field
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, PromptRoles, Message, ROLE_KEY, CONTENT_KEY
from tgen.pipeline.state import State
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder


@dataclass
class ChatState(State):
    user_chat_history: List[MessageMeta] = required_field(field_name="user_chat_history")  # contains only user + llm messages
    context_artifact_types: List[str] = field(default_factory=list)  # layer ids to use for context
    related_artifact_ids: Set[str] = field(default_factory=set)  # all artifact ids used for context

    system_prompt: str = field(init=False, default=None)  # contains context for chat
    internal_chat_history: List[MessageMeta] = field(init=False, default_factory=list)  # contains messages used internally for state
    user_query: str = field(init=False, default=None)  # most recent user message

    def __post_init__(self) -> None:
        """
        Performs post initialize operations.
        :return: None
        """
        if len(self.user_chat_history) > 1:
            self.internal_chat_history = deepcopy(self.user_chat_history[:-1])
        self.user_query = self.user_chat_history[-1].message[CONTENT_KEY]

    def update_related_artifact_ids(self, additional_artifact_ids: Set[str], artifact_df: ArtifactDataFrame,
                                    llm_manager: AbstractLLMManager) -> Set[str]:
        """
        Adds artifact ids to related artifact ids and updates the system prompt.
        :param additional_artifact_ids: Artifact ids to add to related artifact ids.
        :param artifact_df: Contains the project artifacts.
        :param llm_manager: The llm manager to use for the chat.
        :return: The related artifact ids
        """
        self.related_artifact_ids.update(additional_artifact_ids)
        self.update_system_prompt(artifact_df, llm_manager)
        return self.related_artifact_ids

    def update_system_prompt(self, artifact_df: ArtifactDataFrame, llm_manager: AbstractLLMManager) -> str:
        """
        Adds context to message.
        :param artifact_df: Contains the project artifacts.
        :param llm_manager: The llm manager to use for the chat.
        :return: The system's prompt string for the context.
        """
        context_artifacts = [artifact_df.get_artifact(a_id) for a_id in self.related_artifact_ids]
        context_prompt = MultiArtifactPrompt(prompt_start=f"The related information is provided to help you better understand "
                                                          f"and respond to the following question. "
                                                          f"If you do not need the information to respond,"
                                                          f"you may ignore it.",
                                             prompt_args=PromptArgs(title="Related Information", system_prompt=True),
                                             build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                             include_ids=True)
        prompt = PromptBuilder(prompts=[context_prompt]).build(model_format_args=llm_manager.prompt_args,
                                                               artifacts=context_artifacts)
        if prompt[PromptKeys.SYSTEM]:
            self.system_prompt = prompt[PromptKeys.SYSTEM]
        else:
            self.system_prompt = prompt[PromptKeys.PROMPT]
        return self.system_prompt

    def add_internal_chat_message(self, message_content: str, role: str = PromptRoles.USER) -> List[MessageMeta]:
        """
        Add new chat message to the internal chat history.
        :param message_content: Content of new message.
        :param role: Role of speaker of the message.
        :return: Current internal chat history.
        """
        return self._add_chat_message(self.internal_chat_history, message_content, role)

    def add_user_chat_message(self, message_content: str, role: str = PromptRoles.USER) -> List[MessageMeta]:
        """
        Add new chat message to the internal chat history.
        :param message_content: Content of new message.
        :param role: Role of speaker of the message.
        :return: Current internal chat history.
        """
        return self._add_chat_message(self.user_chat_history, message_content, role)

    @staticmethod
    def _add_chat_message(chat_history: List[MessageMeta], message_content: str, role: str = PromptRoles.USER) -> List[MessageMeta]:
        """
        Add new chat message to the chat history.
        :param chat_history: The chaat history to add a new message to.
        :param message_content: Content of new message.
        :param role: Role of speaker of the message.
        :return: Current chat history.
        """
        if len(chat_history) > 0:
            assert role != chat_history[-1].message[ROLE_KEY], "New message cannot be the same role as the last one"
        meta = MessageMeta(message=Message(content=message_content, role=role))
        chat_history.append(meta)
        return chat_history
