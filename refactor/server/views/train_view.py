from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from jobs.responses.base_response import BaseResponse
from jobs.train_job import TrainJob
from server.serializers.training_request_serializer import TrainingRequestSerializer
from server.views.abstract_trace_view import AbstractTraceView


class TrainView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])
    serializer = TrainingRequestSerializer

    def __init__(self, **kwargs):
        super().__init__(self.serializer, TrainJob, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=serializer, responses=responses)
    def post(self, request: HttpRequest):
        return self.run_job(request)
