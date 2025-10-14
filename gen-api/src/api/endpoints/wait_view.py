import time
from typing import TypedDict

from rest_framework import serializers

from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.handler.endpoint_decorator import endpoint
from gen_common.infra.t_logging.logger_manager import logger


class WaitPayload(TypedDict):
    """
    The input to a wait endpoint.
    """
    seconds: int


class WaitPayloadSerializer(AbstractSerializer):
    seconds: serializers.IntegerField()

    def create(self, validated_data):
        """
        Creates dummy payload.
        :param validated_data: The request input data.
        :return: Wait endpoint input.
        """
        return self.initial_data


@endpoint(WaitPayloadSerializer, is_async=True)
def perform_wait(wait_payload: WaitPayload):
    """
    Performs a wait of specified seconds.
    :param wait_payload: The payload defining how many seconds to wait.
    :return: JSON body notifying doneness.
    """
    wait_time = wait_payload["seconds"]
    interval = wait_payload.get("interval", 10)

    for i in range(wait_time):
        time.sleep(1)
        if i % interval == 0:
            logger.info("Cycle...")

    logger.info("Done")
    return {"status": "Done"}
