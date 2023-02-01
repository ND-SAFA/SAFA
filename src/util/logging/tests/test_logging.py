import unittest
from logging import FileHandler
from unittest import skip

from testres.base_test import BaseTest
from train.trainer_tools.trace_accelerator import TraceAccelerator
from util.file_util import FileUtil
from util.logging.logger_manager import logger


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
            TraceAccelerator.is_main_process = is_main_process
            logger.info(msg)
            file_output = FileUtil.read_file(self.get_log_baseFilename())
            self.assertEqual(msg in file_output, is_main_process)

        assert_log_only_if_main_thread(False)
        assert_log_only_if_main_thread(True)

    def get_log_baseFilename(self):
        file_handler = None
        for handler in logger.handlers:
            if isinstance(handler, FileHandler):
                file_handler = handler
                break
        self.assertTrue(file_handler is not None)
        return file_handler.baseFilename