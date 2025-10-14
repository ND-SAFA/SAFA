from unittest import TestCase

from gen_common.infra.t_logging.log_capture import LogCapture
from gen_common.infra.t_logging.logger_manager import logger


def perform_log(log_message):
    logger.info(log_message)


class TestLoggingRetrieval(TestCase):
    """
    Tests that logs are able to be retrieved.
    """

    def test_retrieve(self):
        """
        Tests that logs are captured
        """
        log_capture = LogCapture()
        log_capture.clear()
        perform_log("Test message")
        statements = log_capture.get_logs()
        self.assertEqual(len(statements), 1)
