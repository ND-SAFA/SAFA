from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from jobs.predict_job import PredictJob
from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer
from jobs.results.job_result import JobResult
from server.views.abstract_trace_view import AbstractTraceView


class PredictView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([JobResult.MODEL_PATH, JobResult.STATUS, JobResult.EXCEPTION])
    serializer = PredictionRequestSerializer

    def __init__(self, **kwargs):
        super().__init__(self.serializer, PredictJob, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=serializer, responses=responses)
    def post(self, request: HttpRequest):
        return self.run_job(request)
