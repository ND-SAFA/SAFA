import os

from common.config.constants import IS_TEST
from common.storage.gcp_cloud_storage import GCPCloudStorage


class SafaStorage:
    """
    Contains utility methods for dealing with the current filesystem.
    """

    @staticmethod
    def get_save():
        return SafaStorage._save_to_filesystem if IS_TEST else SafaStorage._save_to_storage

    @staticmethod
    def _save_to_storage(content: str, output_file_path: str):
        """
        Saves output to file at given path in cloud storage solution.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        GCPCloudStorage.upload_file(content, output_file_path)

    @staticmethod
    def _save_to_filesystem(content: str, output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        with SafaStorage.safe_open_w(output_file_path) as file:
            file.write(content)

    @staticmethod
    def safe_open_w(path):
        SafaStorage.create_dir(path)
        return open(path, 'w')

    @staticmethod
    def create_dir(dir_path: str):
        if not os.path.exists(os.path.dirname(dir_path)):
            os.makedirs(os.path.dirname(dir_path))
