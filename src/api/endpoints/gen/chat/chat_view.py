from typing import Dict

from api.endpoints.gen.chat.chat_serializer import ChatSerializer, ChatRequest
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from tgen.chat.message_meta import MessageMeta
from tgen.jobs.chat_jobs.chat_job import ChatJob


@endpoint(ChatSerializer, is_async=True)
def perform_chat(request: ChatRequest) -> Dict:
    """
    Performs a health check on a given artifact.
    :param request: The request containing a dataset for context and the id of the artifact to perform health check on.
    :return: The results of the health check.
    """
    job_args = ViewUtil.create_job_args_from_api_definition(request.dataset)
    job = ChatJob(job_args, chat_history=request.chat_history)
    message_meta: MessageMeta = ViewUtil.run_job(job)
    return {"response": message_meta.message["content"], "related_artifacts": message_meta.artifact_ids}
