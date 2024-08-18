from typing import List

from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.llm_tools.tool_models import DEFAULT_FAILURE_RESPONSE, RequestAssistance
from gen_common.graph.nodes.generate_node import AnswerUser
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.llm.abstract_llm_manager import Message, PromptRoles
from gen_common.llm.message_meta import MessageMeta

from gen.chat.args import ChatArgs
from gen.chat.graph import ChatGraph


class ChatJob(AbstractJob):
    UNKNOWN_RESPONSE = f"I'm sorry but I was unable to find the answer to your question."
    ERROR_RESPONSE = "A problem occurred while generating the response. Please try again."

    def __init__(self, job_args: JobArgs, chat_history: List[MessageMeta], **other_chat_args):
        """
        Initializes the job with the previous chats.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param chat_history: List containing previous conversation, with the last item containing most recent user query.
        :param other_chat_args: The other args for the chat.
        """
        super().__init__(job_args, require_data=True)
        self.chat_history = chat_history
        self.other_chat_args = other_chat_args

    def _run(self) -> MessageMeta:
        """
        Runs the job to get the next response from the LLM.
        :return: The next response from the LLM.
        """
        other_args = self.job_args.get_args_for_pipeline(ChatArgs)
        other_args.update(self.other_chat_args)
        chat_history = MessageMeta.to_langchain_messages(self.chat_history[:-1])
        user_question = self.chat_history[-1].message["content"]

        args = GraphArgs(chat_history=chat_history, user_question=user_question, **other_args)
        runner = ChatGraph.get_runner()
        response_obj = runner.run(args)

        meta = self._meta_from_response(response_obj)

        return meta

    def _meta_from_response(self, response_obj: AnswerUser | RequestAssistance | None) -> MessageMeta:
        """
        Creates a message meta object from the LLM's response.
        :param response_obj: The response object (either answering question or requesting assistance).
        :return: The message meta object.
        """
        match response_obj:
            case AnswerUser(answer=answer, reference_ids=reference_ids):
                meta = MessageMeta(artifact_ids=reference_ids, message=self._response_to_message(answer))
            case RequestAssistance(relevant_information_learned=relevant_information_learned, related_doc_ids=related_doc_ids):
                response = self.UNKNOWN_RESPONSE
                if relevant_information_learned != DEFAULT_FAILURE_RESPONSE:
                    response = f"{response} However, here is a summary of what I was able to learn " \
                               f"that might help you find the answer.\n{relevant_information_learned}"
                meta = MessageMeta(artifact_ids=related_doc_ids, message=self._response_to_message(response))
            case _:
                meta = MessageMeta(message=self._response_to_message(self.ERROR_RESPONSE))
        return meta

    @staticmethod
    def _response_to_message(content: str) -> Message:
        """
        Converts the response from the model to expected message obj.
        :param content: Content of the response.
        :return: The message.
        """
        return Message(content=content, role=PromptRoles.ASSISTANT)
