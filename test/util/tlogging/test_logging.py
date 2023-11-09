import logging
from logging import FileHandler
from unittest import skip, mock
from unittest.mock import MagicMock

from tgen.common.logging.tgen_logger import TGenLogger
from tgen.testres.base_tests.base_test import BaseTest
from tgen.common.util.file_util import FileUtil
from tgen.common.logging.logger_manager import logger


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

    @mock.patch.object(TGenLogger, "_log")
    def test_log_once(self, log_mock: MagicMock = None):
        msg_1 = "Unable to parse"
        msg_2 = "This is a new problem"
        logger.log_without_spam(level=logging.WARNING, msg=msg_1)
        logger.log_without_spam(level=logging.WARNING, msg=msg_1)
        logger.log_without_spam(level=logging.WARNING, msg=msg_1)
        logger.log(level=logging.WARNING, msg=msg_2)
        logger.log(level=logging.WARNING, msg=msg_2)
        logger.log_without_spam(level=logging.WARNING, msg=msg_1)
        logger.log_without_spam(level=logging.WARNING, msg=msg_2)
        logger.log_without_spam(level=logging.WARNING, msg=msg_1)
        msgs = [call[0][1] for call in log_mock.call_args_list]
        self.assertSize(5, msgs)
        self.assertListEqual([msg_1, msg_2, msg_2, msg_2, msg_1], msgs)

    def get_log_baseFilename(self):
        file_handler = None
        for handler in logger.handlers:
            if isinstance(handler, FileHandler):
                file_handler = handler
                break
        self.assertTrue(file_handler is not None)
        return file_handler.baseFilename
