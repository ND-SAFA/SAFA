import unittest
from logging import FileHandler
from unittest.mock import patch

from testres.base_test import BaseTest
from testres.paths.paths import TEST_OUTPUT_DIR
from train.trainer_tools.trace_accelerator import TraceAccelerator
from util.file_util import FileUtil
from util.logging.logger_config import LoggerConfig
from util.logging.logger_manager import LoggerManager, logger


class TestLogging(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestLogging, cls).setUpClass()
        config = LoggerConfig(output_dir=TEST_OUTPUT_DIR)
        LoggerManager.configure_logger(config)

    @classmethod
    def tearDownClass(cls):
        super(TestLogging, cls).tearDownClass()
        BaseTest.remove_output_dir()

    def test_log_with_title(self):
        title, msg = "Title", "message"
        logger.log_with_title(title, msg)
        file_output = FileUtil.read_file(self.get_log_baseFilename())
        self.assertIn(title, file_output)
        self.assertIn(msg, file_output)

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
