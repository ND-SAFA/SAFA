import os
import shutil

from django.test import TestCase

from common.config.constants import DELETE_TEST_OUTPUT
from common.storage.safa_storage import SafaStorage
from test.config.paths import TEST_OUTPUT_DIR


class BaseTest(TestCase):
    def setup(self):
        if not os.path.isdir(TEST_OUTPUT_DIR):
            SafaStorage.create_dir(TEST_OUTPUT_DIR)

    def tearDown(self):
        if DELETE_TEST_OUTPUT:
            for file in os.listdir(TEST_OUTPUT_DIR):
                file_path = os.path.join(TEST_OUTPUT_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)
