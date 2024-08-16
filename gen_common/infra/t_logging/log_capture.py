import logging
from typing import List

from gen_common.constants import NEW_LINE, EMPTY_STRING

global tqdm_log_capture


class LogCapture(logging.Handler):
    """
    Stores logs in list making accessible for sending between API requests.
    """
    _instance = None

    def __init__(self):
        """
        Constructs empty capture.
        """
        super().__init__()
        self.logs = []
        self.current_entry = ""
        self.register()

    def clear(self) -> None:
        """
        Clears the state of the capture.
        :return: None
        """
        self.logs = []
        self.current_entry = ""

    def get_log(self, delimiter: str = NEW_LINE) -> str:
        """
        Returns single log containing all captured logs.
        :param delimiter: The delimiter used between log statements.
        :return: String representing log.
        """
        return delimiter.join(self.logs)

    def get_logs(self) -> List[str]:
        """
        Returns all logs captured.
        :return: List of logs.
        """
        return self.logs

    def emit(self, record):
        """
        Extends log emission to store record.
        :param record: The log being emitted.
        :return: None
        """
        entry = self.format(record)
        self.add_entry(entry)

    def add_entry(self, *entries: str, delimiter: str = EMPTY_STRING) -> None:
        """
        Records log to capture.
        :param entries: The log to capture.
        :param delimiter: Separates the entries.
        :return: None
        """
        entry = delimiter.join(filter(lambda e: e is not None, entries))
        if len(entry) > 0:
            self.logs.append(entry)

    def register(self, logger=None):
        """
        Registers capture to root logger.
        :param logger: The logger used to register handler with.
        :return:
        """
        if logger is None:
            logger = logging.getLogger()
        logger.addHandler(self)
