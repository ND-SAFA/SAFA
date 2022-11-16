from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from jobs.mlm_pre_train_job import MLMPreTrainJob
from jobs.responses.base_response import BaseResponse
from server.serializers.job_factory.pre_training_request_serializer import PreTrainingRequestSerializer
from server.views.abstract_trace_view import AbstractTraceView


class PreTrainView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])
    serializer = PreTrainingRequestSerializer

    def __init__(self, **kwargs):
        super().__init__(self.serializer, MLMPreTrainJob, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=serializer, responses=responses)
    def post(self, request: HttpRequest):
        return self.run_job(request)
