from typing import Dict

from api.endpoints.gen.chat.chat_serializer import ChatRequest, ChatSerializer
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from tgen.chat.message_meta import MessageMeta
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.jobs.chat_jobs.chat_job import ChatJob

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
    job = ChatJob(job_args, chat_history=request.chat_history, system_prompt=PROMPT)
    response_message: MessageMeta = ViewUtil.run_job(job)
    response = response_message.message["content"]
    title = LLMResponseUtil.parse(response, PROMPT_TAG)
    return {PROMPT_TAG: title}
