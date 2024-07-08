import json
from typing import Callable, Dict, List, Union

from django.test import Client

from api.endpoints.auth_view import AUTH_KEY
from api.endpoints.gen.serializers.message_serializer import MessageDTO
from api.server.app_endpoints import AppEndpoints
from apiTests.base_test import BaseTest
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.json_util import NpEncoder
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.summary_jobs.summary_response import SummaryResponse


class RequestProxy:
    CLIENT = None

    @staticmethod
    def chat(dataset: ApiDefinition, chat_history: List[MessageDTO], endpoint=AppEndpoints.CHAT) -> List[Trace]:
        """
        Creates chat with the model.
        :param dataset: The dataset containing project artifacts for context.
        :param chat_history: List of messages exchanged with the model.
        :param endpoint: The endpoint to send data to.
        :return: The model response and any artifacts used for context.
        """
        data = {"dataset": dataset, "chat_history": chat_history}
        response = RequestProxy._request(endpoint, data)
        return response

    @staticmethod
    def health(dataset: ApiDefinition, query_id: str, concept_layer_id: str) -> List[Trace]:
        """
        Performs health checks on the query artifact.
        :param dataset: The dataset containing project artifacts for context.
        :param query_id: The id of the query artifact under inspection.
        :param concept_layer_id: The id of the layer containing concept artifacts.
        :return: The health check results.
        """
        data = {"dataset": dataset, "query_ids": [query_id], "concept_layer_id": concept_layer_id}
        response = RequestProxy._request(AppEndpoints.HEALTH, data)
        return response

    @staticmethod
    def trace(dataset: ApiDefinition, sync=False) -> List[Trace]:
        """
        Traces the layers defined in given api definition.
        :param dataset: The dataset containing artifacts and layers to trace.
        :param sync: Whether to trace syncronously.
        :return: The list of trace predictions.
        """
        data = {"dataset": dataset}
        suffix = "sync" if sync else None
        response = RequestProxy._request(AppEndpoints.TGEN.as_endpoint(suffix=suffix), data)
        return [Trace(**t) for t in response["predictions"]]

    @staticmethod
    def hgen(artifacts: List[Artifact], target_types: List[str], summary: str = None) -> TraceDataset:
        """
        Generates given target types from artifacts.
        :param artifacts: The source artifacts to generate target types from.
        :param target_types: The types of artifacts to generate.
        :param summary: The project summary.
        :return: Dataset containing source and target artifacts.
        """
        if isinstance(target_types, str):
            target_types = [target_types]
        data = {"artifacts": artifacts, "targetTypes": target_types, "summary": summary}
        response = RequestProxy._request(AppEndpoints.HGEN, data)
        return response

    @staticmethod
    def summarize(artifacts: List[Artifact]) -> SummaryResponse:
        """
        Summarizes artifacts and returns summary response.
        :param artifacts: The artifacts to summarize.
        :return: Artifact summaries and optionally project summary.
        """
        data = {"artifacts": artifacts}
        response = RequestProxy._request(AppEndpoints.SUMMARIZE, data)
        return response

    @staticmethod
    def _request(url: Union[str, AppEndpoints], data: Dict = None, method: str = "POST", content_type="application/json"):
        """
        Requests the application at given url
        :param url: The url to make request for.
        :param data: The data to include in request.
        :param method: The type of request to make.
        :param content_type: The type of content expected to be received.
        :return: The endpoint response.
        """
        if isinstance(url, AppEndpoints):
            url = url.as_endpoint()
        client_method = RequestProxy.get_client_method(method)
        data = json.loads(json.dumps(data, cls=NpEncoder))
        data[AUTH_KEY] = BaseTest.API_KEY
        response = client_method(url, data=data, content_type=content_type)
        if response.status_code >= 300:
            raise Exception(response.content)
        return json.loads(response.content)

    @classmethod
    def get_client_method(cls, method: str) -> Callable:
        """
        Creates django server client singleton and returns method associated with that singleton.
        :param method: The HTTP request type for method to retrieve.
        :return: The callable of client representing method type.
        """
        if cls.CLIENT is None:
            cls.CLIENT = Client()
        c = cls.CLIENT
        methods = {
            "POST": c.post,
            "GET": c.get
        }
        assert method in methods, f"Expected method to be one of: {methods.keys()}"
        return methods[method]
