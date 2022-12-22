from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from jobs.components.job_result import JobResult
from jobs.delete_model_job import DeleteModelJob
from server.serializers.experiment_serializer import ExperimentSerializer
from server.views.abstract_trace_view import AbstractTraceView


class DeleteModelView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([JobResult.MODEL_PATH, JobResult.STATUS, JobResult.EXCEPTION])
    serializer = ExperimentSerializer

    def __init__(self, **kwargs):
        super().__init__(self.serializer, DeleteModelJob, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=serializer, responses=responses)
    def delete(self, request: HttpRequest):
        return self.run_job(request)
