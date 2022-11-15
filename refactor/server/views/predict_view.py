from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from api.responses.base_response import BaseResponse
from jobs.predict_job import PredictJob
from server.serializers.prediction_request_serializer import PredictionRequestSerializer
from server.views.abstract_trace_view import AbstractTraceView


class PredictView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])
    serializer = PredictionRequestSerializer

    def __init__(self, **kwargs):
        super().__init__(self.serializer, PredictJob, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=serializer, responses=responses)
    def post(self, request: HttpRequest):
        return self.run_job(request)
