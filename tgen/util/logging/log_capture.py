import logging
from typing import List


class LogCapture(logging.Handler):
    """
    Stores logs in list making accessible for sending between API requests.
    """

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

    def get_log(self, delimiter: str = "\n") -> str:
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

    def write(self, *args) -> None:
        """
        Overrides writes to std out to add to log. Used for tqdm.
        :param args: Arguments passed to std out.
        :return: None
        """
        entry = "".join(args)
        print(*args, end="")
        self.add_entry(entry)

    def add_entry(self, *entries: str, delimiter="") -> None:
        """
        Records log to capture.
        :param entry: The log to capture.
        :return: None
        """
        entry = delimiter.join(filter(lambda e: e is not None, entries))
        if len(entry) > 0:
            self.logs.append(entry)

    def register(self, logger=None):
        """
        Registers capture to root logger.
        :return:
        """
        if logger is None:
            logger = logging.getLogger()
        logger.addHandler(self)


log_capture = LogCapture()
