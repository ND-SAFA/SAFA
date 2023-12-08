from enum import Enum

from tgen.common.constants.deliminator_constants import EMPTY_STRING, F_SLASH


class AppEndpoints(Enum):
    """
    Enumerates all available endpoints.
    """
    COMPLETE = "complete"
    PROJECT_SUMMARY = "project-summary"
    HGEN = "hgen"
    TGEN = "tgen"
    SUMMARIZE = "summarize"
    STATUS = "status"
    CANCEL = "cancel"
    RESULTS = "results"

    def as_endpoint(self, sync=False) -> str:
        """
        :return: Client endpoint location..
        """
        return self.as_path(prefix=F_SLASH, sync=sync)

    def as_path(self, prefix: str = EMPTY_STRING, sync=False) -> str:
        """
        :return: Internal endpoint location.
        """
        endpoint_value = self.get_name(sync=sync)
        return f"{prefix}{endpoint_value}/"

    def get_name(self, sync: bool = False):
        """
        Returns the value of the endpoint.
        :param sync: Whether to convert the endpoint to a syncronous one.
        :return: The endpoint value.
        """
        internal_value = self.value
        if sync:
            internal_value = f"{internal_value}-sync"
        return internal_value
