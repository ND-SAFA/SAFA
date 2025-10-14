from enum import Enum

from tgen.common.constants.deliminator_constants import EMPTY_STRING, F_SLASH


class AppEndpoints(Enum):
    """
    Enumerates all available endpoints.
    """
    API = "api"
    HGEN = "hgen"
    TGEN = "tgen"
    CHAT = "chat"
    CHAT_TITLE = "chat-title"
    SUMMARIZE = "summarize"
    STATUS = "status"
    CANCEL = "cancel"
    RESULTS = "results"
    WAIT = "wait"
    SYSTEM = "system"
    HEALTH = "health"
    TASKS_ACTIVE = "tasks/active"
    TASKS_PENDING = "tasks/pending"

    def as_endpoint(self, suffix: str = None) -> str:
        """
        Return enumeration as endpoint path.
        :param suffix: The suffix to attach to endpoint.
        :return: Client endpoint location..
        """
        return self.as_path(prefix=F_SLASH, suffix=suffix)

    def as_path(self, prefix: str = EMPTY_STRING, suffix: str = None) -> str:
        """
        Return enum as path in django server.
        :param prefix: The prefix to pre-pend to path.
        :param suffix: The suffix to append to path.
        :return: Internal endpoint location.
        """
        endpoint_value = self.get_name(suffix=suffix)
        return f"{prefix}{endpoint_value}/"

    def get_name(self, suffix: str = None):
        """
        Returns the value of the endpoint.
        :param suffix: The suffix to add to endpoint.
        :return: The endpoint value.
        """
        internal_value = self.value
        if suffix:
            internal_value = f"{internal_value}-{suffix}"
        return internal_value
