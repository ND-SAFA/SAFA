from typing import Dict

from api.endpoints.gen.chat.chat_serializer import ChatRequest, ChatSerializer
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from gen.chat.chat_job import ChatJob
from gen_common.llm.message_meta import MessageMeta


@endpoint(ChatSerializer, is_async=True)
def perform_chat(request: ChatRequest) -> Dict:
    """
    Performs a health check on a given artifact.
    :param request: The request containing a dataset for context and the id of the artifact to perform health check on.
    :return: The results of the health check.
    """
    job_args = ViewUtil.create_job_args_from_api_definition(request.dataset)
    job = ChatJob(job_args, chat_history=request.chat_history)
    response: MessageMeta = ViewUtil.run_job(job)
    return {"message": response.message["content"], "artifact_ids": response.artifact_ids}
