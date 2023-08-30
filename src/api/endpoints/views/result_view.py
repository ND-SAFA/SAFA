from typing import Tuple, TypedDict

from celery import states
from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework import serializers

from api.constants.api_constants import MEDIUM_TEXT
from api.constants.celery_status import CeleryStatus
from api.endpoints.base.endpoint import endpoint
from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from tgen.common.util.json_util import NpEncoder
from tgen.common.util.logging.logger_manager import logger


class ResultPayload(TypedDict):
    task_id: str


class ResultSerializer(AbstractSerializer[ResultPayload]):
    task_id = serializers.CharField(max_length=MEDIUM_TEXT, help_text="ID of task.")


def get_task_status(result: AsyncResult.status) -> Tuple[CeleryStatus, str]:
    """
    Returns the current status of the celery result along with human readable message.
    :param result: The task result.
    :return: Task status and message.
    """
    status = result.status
    if status == states.SUCCESS:
        return CeleryStatus.SUCCESS, "Task finished successfully."
    elif status == states.FAILURE:
        return CeleryStatus.FAILURE, result.traceback
    elif status == states.PENDING:
        return CeleryStatus.NOT_STARTED, "Task is pending."
    elif status in [states.STARTED, "PROGRESS"]:
        return CeleryStatus.IN_PROGRESS, "Task is in progress."
    elif status in [states.FAILURE, states.REVOKED, states.REJECTED, states.IGNORED]:
        return CeleryStatus.FAILURE, "Task has failed."
    else:
        raise Exception(f"CeleryStatus is unknown:{result.status}")


def try_get_logs(async_result: AsyncResult):
    try:
        return async_result["logs"]
    except:
        return []


@endpoint(ResultSerializer)
def cancel_job(payload: ResultPayload):
    task_id = payload["task_id"]
    logger.info(f"Cancelling and deleting task: {task_id}")
    result = AsyncResult(task_id)
    res = result.revoke(signal="KILL", terminate=True)
    result.forget()
    return JsonResponse({"status": CeleryStatus.REVOKED, "message": res, "logs": []}, encoder=NpEncoder)


@endpoint(ResultSerializer)
def get_status(payload: ResultPayload):
    task_id = payload["task_id"]
    result = AsyncResult(task_id)
    results_obj = result.result
    logs = try_get_logs(results_obj)
    status, message = get_task_status(result)
    status_dict = {"status": status, "message": message, "logs": logs}
    return JsonResponse(status_dict, encoder=NpEncoder)


@endpoint(ResultSerializer)
def get_result(payload: ResultPayload):
    task_id = payload["task_id"]
    result = AsyncResult(task_id)

    if result.successful():
        job_result = result.result
        result.forget()
        return job_result
    else:
        status, msg = get_status(payload)
        return JsonResponse({"error": f"Job status: {msg}"}, status=400)
