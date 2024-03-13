from typing import Dict, List, Tuple, TypedDict, Union

from celery import states
from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework import serializers

from api.constants.api_constants import TEXT_MEDIUM
from api.constants.celery_status import CeleryStatus
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.handler.endpoint_decorator import endpoint, endpoint_get
from api.server.celery import celery
from tgen.common.logging.logger_manager import logger
from tgen.common.util.json_util import NpEncoder


class TaskIdentifier(TypedDict):
    """
    Payload for endpoints needing to specify a task.
    """
    task_id: str


class TaskIdentifierSerializer(AbstractSerializer[TaskIdentifier]):
    """
    Serializes task identifiers.
    """
    task_id = serializers.CharField(max_length=TEXT_MEDIUM, help_text="ID of task.")


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
    """
    A hack to try to get the result
    :param async_result:
    :return:
    """
    try:
        return async_result["logs"]
    except:
        return []


@endpoint(TaskIdentifierSerializer)
def cancel_job(task_identifier: TaskIdentifier):
    """
    Cancels the task.
    :param task_identifier: Contains ID of task to cancel.
    :return: The new status of the task.
    """
    task_id = task_identifier["task_id"]
    logger.info(f"Cancelling and deleting task: {task_id}")
    result = AsyncResult(task_id)
    res = result.revoke(signal="KILL", terminate=True)
    result.forget()
    return JsonResponse({"status": CeleryStatus.REVOKED, "message": res, "logs": []}, encoder=NpEncoder)


@endpoint(TaskIdentifierSerializer)
def get_status(task_identifier: TaskIdentifier) -> JsonResponse:
    """
    Returns the status of the task.
    :param task_identifier: Contains ID of task whose status is queried.
    :return: Status of task.
    """
    task_id = task_identifier["task_id"]
    result = AsyncResult(task_id)
    results_obj = result.result
    logs = try_get_logs(results_obj)
    status, message = get_task_status(result)
    status_dict = {"status": status, "message": message, "logs": logs}
    return JsonResponse(status_dict, encoder=NpEncoder)


@endpoint(TaskIdentifierSerializer)
def get_result(task_identifier: TaskIdentifier) -> Union[Dict, JsonResponse]:
    """
    Gets the result of the task
    :param task_identifier: Contains task ID of result to return.
    :return: The result of the Job.
    """
    task_id = task_identifier["task_id"]
    result = AsyncResult(task_id)

    if result.successful():
        job_result = result.result
        result.forget()
        return job_result
    else:
        status, msg = get_status(task_identifier)
        return JsonResponse({"error": f"Job status: {msg}"}, status=400)


@endpoint_get
def get_active_task_ids() -> Dict:
    """
    :return: List of active task IDs.
    """
    i = celery.control.inspect()
    active_task_map = i.active()

    return {"active_task_ids": get_task_ids(active_task_map)}


@endpoint_get
def get_pending_task_ids() -> Dict:
    """
    :return: List of pending task IDs.
    """
    i = celery.control.inspect()
    active_task_map = i.reserved()
    return {"pending_task_ids": get_task_ids(active_task_map)}


def get_task_ids(queue2tasks: Dict) -> List[str]:
    """
    Returns the set of task IDs in map.
    :param queue2tasks: Map of queue to tasks in celery app.
    :return: List of task ids.
    """
    task_ids = [task["id"] for queue, queue_tasks in queue2tasks.items() for task in queue_tasks]
    return task_ids
