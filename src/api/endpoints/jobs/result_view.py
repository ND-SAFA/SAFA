from celery.result import AsyncResult
from rest_framework import serializers
from rest_framework.views import APIView

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.views.endpoint import endpoint


class ResultSerializer(AbstractSerializer):
    task_id = serializers.CharField(max_length=1028, help_text="ID of task.")


class ResultView(APIView):
    @endpoint(ResultSerializer)
    def post(self, payload):
        task_id = payload["task_id"]
        result = AsyncResult(task_id)
        if result.ready():
            # Task has been executed and the result is ready
            task_result = result.result  # Retrieve the actual result value
        else:
            task_result = "Task is still running"
        return lambda: {"result": task_result}
