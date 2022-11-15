from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from api.responses.base_response import BaseResponse
from jobs.create_model_job import CreateModelJob
from server.serializers.model_identifier_serializer import ModelIdentifierSerializer
from server.views.abstract_trace_view import AbstractTraceView


class CreateModelView(AbstractTraceView):
    """
    Provides endpoint for creating a new model.
    """

    responses = AbstractTraceView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @csrf_exempt
    @swagger_auto_schema(request_body=ModelIdentifierSerializer, responses=responses)
    def post(self, request: HttpRequest):
        model_identifier = self.read_request(request, ModelIdentifierSerializer)
        create_model_job = CreateModelJob(model_path=model_identifier.model_path,
                                          output_dir=model_identifier.output_dir,
                                          add_mount_directory_to_output=model_identifier.load_from_storage)
        return create_model_job.run()
