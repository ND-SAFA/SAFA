import logging
from logging import FileHandler
from unittest import mock, skip
from unittest.mock import MagicMock

from gen_common.infra.t_logging.logger_manager import logger
from gen_common.infra.t_logging.the_logger import TheLogger
from gen_common.util import FileUtil
from gen_common_test.base_tests.base_test import BaseTest


class TestLogging(BaseTest):

    @skip("Can only be run solo due to other tests deleting the output dir prematurely")
    def test_log_with_title(self):
        title, msg = "Title", "message"
        logger.log_with_title(title, msg)
        file_output = FileUtil.read_file(self.get_log_baseFilename())
        self.assertIn(title, file_output)
        self.assertIn(msg, file_output)

    @skip("Can only be run solo due to other tests deleting the output dir prematurely")
    def test_log_only_if_main_thread(self):
        msg = "Should not log"

        def assert_log_only_if_main_thread(is_main_process):
            # TraceAccelerator.is_main_process = is_main_process
            logger.info(msg)
            file_output = FileUtil.read_file(self.get_log_baseFilename())
            self.assertEqual(msg in file_output, is_main_process)

        # assert_log_only_if_main_thread(False)
        assert_log_only_if_main_thread(True)

    @mock.patch.object(TheLogger, "_log")
    def test_log_once(self, log_mock: MagicMock = None):
        log_memory = 5
        for i in range(2 * log_memory):
            logger.log_without_spam(logging.WARNING, f"msg{i % log_memory}")
        self.assertEqual(log_mock.call_count, log_memory)
        logger.log_without_spam(logging.WARNING, "another one")
        logger.log_without_spam(logging.WARNING, "msg0")
        self.assertEqual(log_mock.call_count, log_memory + 2)

    def get_log_baseFilename(self):
        file_handler = None
        for handler in logger.handlers:
            if isinstance(handler, FileHandler):
                file_handler = handler
                break
        self.assertTrue(file_handler is not None)
        return file_handler.baseFilename
