from typing import Dict, List

from api.endpoints.gen.chat.chat_serializer import ChatRequest, ChatSerializer
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from tgen.chat.message_meta import MessageMeta
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.jobs.chat_jobs.chat_job import ChatJob
from tgen.models.llm.abstract_llm_manager import Message

PROMPT_TAG = "title"
PROMPT = f"Please give this chat a title enclosed in <{PROMPT_TAG}></{PROMPT_TAG}>."


@endpoint(ChatSerializer, is_async=False)
def perform_chat_name(request: ChatRequest) -> Dict:
    """
    Performs a health check on a given artifact.
    :param request: The request containing a dataset for context and the id of the artifact to perform health check on.
    :return: The results of the health check.
    """
    job_args = ViewUtil.create_job_args_from_api_definition(request.dataset)
    prompt_message = Message(role="user", content=PROMPT)
    title_message = MessageMeta(message=prompt_message, artifact_ids=[])

    chat_history = retrieve_valid_chat_history(request.chat_history)
    chat_history.append(title_message)

    job = ChatJob(job_args, chat_history=chat_history)

    response_message: MessageMeta = ViewUtil.run_job(job)
    response = response_message.message["content"]
    title = LLMResponseUtil.parse(response, PROMPT_TAG)[0]
    return {PROMPT_TAG: title}


def retrieve_valid_chat_history(chat_history: List[MessageMeta]) -> List[MessageMeta]:
    """
    Returns chat history up until the last assistant message.
    :param chat_history: Chat history.
    :return: Chat history ending with assistant message.
    """
    assistant_message_indices = [i for i, chat in enumerate(chat_history) if chat.message["role"] == "assistant"]
    if len(assistant_message_indices) == 0:
        raise ValueError("No assistant messages found.")
    last_assistant_message_index = max(assistant_message_indices)
    return chat_history[:last_assistant_message_index + 1]
