from typing import Any, List, Set

from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_state import ChatState
from tgen.chat.chat_state_machine import ChatStateMachine
from tgen.chat.message_meta import MessageMeta
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager


class ChatJob(AbstractJob):

    def __init__(self, job_args: JobArgs, chat_history: List[MessageMeta], llm_manager: AbstractLLMManager = None,
                 max_context: int = None):
        """
        Initializes the job with the previous chats.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param chat_history: List containing previous conversation, with the last item containing most recent user query.
        :param llm_manager: Responsible for making LLM responses.
        :param max_context: The max number of artifacts to include in the context for the model.
        """
        super().__init__(job_args, require_data=True)
        self.chat_history = chat_history
        self.llm_manager = llm_manager
        self.max_context = max_context

    def _run(self) -> Any:
        """
        Runs the job to get the next response from the LLM.
        :return: The next response from the LLM.
        """
        other_args = self.job_args.get_args_for_pipeline(ChatArgs)
        chat_args = ChatArgs(chat_history=self.chat_history,
                             max_context=self.max_context,
                             **other_args)
        if self.llm_manager:
            chat_args.llm_manager = self.llm_manager
        path = ChatStateMachine(chat_args).run()
        state: ChatState = path.state
        meta = state.user_chat_history[-1]
        meta.artifact_ids = state.user_chat_history[-2].artifact_ids
        return meta

