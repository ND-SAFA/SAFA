from typing import TypedDict

from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.views.endpoint import endpoint


class ResultPayload(TypedDict):
    task_id: str


class ResultSerializer(AbstractSerializer[ResultPayload]):
    task_id = serializers.CharField(max_length=1028, help_text="ID of task.")


@endpoint(ResultSerializer)
def retrieve_result(payload: ResultPayload):
    task_id = payload["task_id"]
    result = AsyncResult(task_id)
    if not result.successful():
        return JsonResponse({"error": result.traceback}, status=400)
    if result.ready():
        # Task has been executed and the result is ready
        task_result = result.result  # Retrieve the actual result value
    else:
        task_result = "Task is still running"
    return task_result
