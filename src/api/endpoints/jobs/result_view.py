from typing import TypedDict

from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.views.endpoint import endpoint
from tgen.util.status import Status


class ResultPayload(TypedDict):
    task_id: str


class ResultSerializer(AbstractSerializer[ResultPayload]):
    task_id = serializers.CharField(max_length=1028, help_text="ID of task.")


def get_task_status(result):
    if result.successful():
        return Status.SUCCESS, "Task finished successfully"
    elif result.failed():
        return Status.FAILURE, "Task finished with an error"
    elif result.status == "PENDING":
        return Status.NOT_STARTED, "Task is still pending"
    elif result.status == "STARTED":
        return Status.IN_PROGRESS, "Task is still running"
    else:
        raise Exception(f"Status is unknown:{result.status}")


@endpoint(ResultSerializer)
def get_status(payload: ResultPayload):
    task_id = payload["task_id"]
    result = AsyncResult(task_id)
    status, msg = get_task_status(result)
    return {"status": status, "message": msg}


@endpoint(ResultSerializer)
def get_result(payload: ResultPayload):
    task_id = payload["task_id"]
    result = AsyncResult(task_id)

    if result.successful():
        return result.result
    else:
        status, msg = get_status(payload)
        return JsonResponse({"error": f"Job status: {msg}"}, status=400)
