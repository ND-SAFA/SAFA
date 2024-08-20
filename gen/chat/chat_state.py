from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Set

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.llm.abstract_llm_manager import AbstractLLMManager, CONTENT_KEY, Message, PromptRoles
from gen_common.llm.message_meta import MessageMeta
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.pipeline.state import State
from gen_common.util.dataclass_util import required_field
from gen_common.util.pythonisms_util import default_mutable


@dataclass
class ChatState(State):
    user_chat_history: List[MessageMeta] = required_field(field_name="user_chat_history")  # contains only user + llm messages
    context_artifact_types: Set[str] = field(default_factory=set)  # layer ids to use for context
    related_artifact_ids: Set[str] = field(default_factory=set)  # all artifact ids used for context

    system_prompt: str = field(init=False, default=None)  # contains context for chat
    internal_chat_history: List[MessageMeta] = field(init=False, default_factory=list)  # contains messages used internally for state
    user_query: str = field(init=False, default=None)  # most recent user message
    rewritten_query: str = None

    def __post_init__(self) -> None:
        """
        Performs post initialize operations.
        :return: None
        """
        index_of_user_message = MessageMeta.index_of_last_response_from_role(self.user_chat_history, role=PromptRoles.USER)
        assert index_of_user_message >= 0, "Chat history most include at least one message from the user."
        self.user_query = self.user_chat_history[index_of_user_message].message[CONTENT_KEY]
        if index_of_user_message > 0:
            self.internal_chat_history = deepcopy(self.user_chat_history[:index_of_user_message])

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

    def add_internal_chat_message(self, message_content: str, role: str = PromptRoles.USER,
                                  replace_last: bool = False) -> List[MessageMeta]:
        """
        Add new chat message to the internal chat history.
        :param message_content: Content of new message.
        :param role: Role of speaker of the message.
        :param replace_last: If True, replaces the last message instead of just appending.
        :return: Current internal chat history.
        """
        return self.add_chat_message(message_content, self.internal_chat_history, role, replace_last=replace_last)

    def add_user_chat_message(self, message_content: str, role: str = PromptRoles.USER,
                              replace_last: bool = False) -> List[MessageMeta]:
        """
        Add new chat message to the internal chat history.
        :param message_content: Content of new message.
        :param role: Role of speaker of the message.
        :param replace_last: If True, replaces the last message instead of just appending.
        :return: Current internal chat history.
        """
        return self.add_chat_message(message_content, self.user_chat_history, role, replace_last=replace_last)

    @staticmethod
    @default_mutable()
    def add_chat_message(message_content: str, chat_history: List[MessageMeta] = None, role: str = PromptRoles.USER,
                         replace_last: bool = False) -> List[MessageMeta]:
        """
        Add new chat message to the chat history.
        :param chat_history: The chat history to add a new message to.
        :param message_content: Content of new message.
        :param role: Role of speaker of the message.
        :param replace_last: If True, replaces the last message instead of just appending.
        :return: Current chat history.
        """
        if chat_history:
            if MessageMeta.is_message_from_role(chat_history, role):
                assert replace_last, "New message cannot be the same role as the last one"
            else:
                replace_last = False  # Do not need to replace last because it was not from the same role

            if replace_last:
                chat_history.pop()

        meta = MessageMeta(message=Message(content=message_content, role=role))
        chat_history.append(meta)
        return chat_history
