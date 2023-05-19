from rest_framework import serializers
from rest_framework.views import APIView

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.tasks import add_task


class JobSerializer(AbstractSerializer):
    job_name = serializers.CharField(max_length=1028, help_text="The name of the job to run.")


class JobView(APIView):
    @endpoint(JobSerializer)
    def post(self, job):
        task = add_task.delay(3, 4)  # Delayed execution of the task
        return lambda: task.id, lambda t_id: {"task_id": t_id}
