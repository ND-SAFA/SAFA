from typing import Dict

from api.endpoints.handler.ihandler import IHandler


class SyncEndpointHandler(IHandler):
    def _request_handler(self, data: Dict) -> Dict:
        """
        Performs endpoint function on data.
        :param data: The request data.
        :return: Output of endpoint function.
        """
        return self.func(data)
