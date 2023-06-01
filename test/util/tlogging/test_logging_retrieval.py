from unittest import TestCase

from tqdm import tqdm

from tgen.util.logging.log_capture import log_capture
from tgen.util.logging.logger_manager import logger


def perform_log(log_message):
    logger.info(log_message)


def perform_tqdm(n_items):
    sum = 0
    for i in tqdm(range(n_items)):
        sum += i


class TestLoggingRetrieval(TestCase):
    """
    Tests that logs are able to be retrieved.
    """

    def test_retrieve(self):
        """
        Tests that logs are captured
        """
        log_capture.clear()
        perform_log("Test message")
        perform_tqdm(10)
        statements = log_capture.get_logs()
        self.assertEqual(len(statements), 4)
