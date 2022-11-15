from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from api.responses.base_response import BaseResponse
from jobs.delete_model_job import DeleteModelJob
from server.serializers.model_identifier_serializer import ModelIdentifierSerializer
from server.views.abstract_trace_view import AbstractTraceView


class DeleteModelView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])
    serializer = ModelIdentifierSerializer

    def __init__(self, **kwargs):
        super().__init__(self.serializer, DeleteModelJob, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=serializer, responses=responses)
    def delete(self, request: HttpRequest):
        return self.run_job(request)
