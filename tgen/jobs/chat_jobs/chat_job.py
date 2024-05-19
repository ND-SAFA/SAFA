from typing import Any, List

from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_state import ChatState
from tgen.chat.chat_state_machine import ChatStateMachine
from tgen.chat.message_meta import MessageMeta
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class ChatJob(AbstractJob):

    def __init__(self, job_args: JobArgs, chat_history: List[MessageMeta], nodes2skip: List[str] = None,
                 **other_chat_args):
        """
        Initializes the job with the previous chats.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param chat_history: List containing previous conversation, with the last item containing most recent user query.
        :param nodes2skip: Set of node ids that should be skipped.
        :param other_chat_args: The other args for the chat.
        """
        super().__init__(job_args, require_data=True)
        self.chat_history = chat_history
        self.other_chat_args = other_chat_args
        self.nodes2skip = set(nodes2skip) if nodes2skip else nodes2skip

    def _run(self) -> Any:
        """
        Runs the job to get the next response from the LLM.
        :return: The next response from the LLM.
        """
        other_args = self.job_args.get_args_for_pipeline(ChatArgs)
        other_args.update(self.other_chat_args)
        chat_args = ChatArgs(chat_history=self.chat_history,
                             **other_args)
        path = ChatStateMachine(chat_args, nodes2skip=self.nodes2skip).run()
        state: ChatState = path.state
        meta = state.user_chat_history[-1]
        meta.artifact_ids = state.user_chat_history[-2].artifact_ids
        return meta
