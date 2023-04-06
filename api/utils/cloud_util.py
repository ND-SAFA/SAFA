import os
from typing import List

from api_constants import MODEL_CACHE_PATH
from cloud.supported_cloud_storage import SupportedCloudStorage


class CloudUtility:
    """
    Contains utility methods for dealing with cloud storage.
    """

    @staticmethod
    def copy_files(src_path: str, dest_path: str, bucket_name: str, ignore: List[str] = None):
        """
        Copies files in directory to folder at destination within bucket.
        :param src_path: The path to directory containing files to copy.
        :param dest_path: The path to the destination within the bucket to save files to.
        :param bucket_name: The bucket to store files in.
        :param ignore: Files to ignore copying over.
        :return: None
        """

        if ignore is None:
            ignore = []
        storage = SupportedCloudStorage.get_storage()

        for file in os.listdir(src_path):
            if file in ignore:
                continue
            file_path = os.path.join(src_path, file)
            export_path = os.path.join(dest_path, file)
            storage.copy(file_path, export_path, bucket_name)

    @staticmethod
    def download_model(model_path: str, bucket_name: str) -> str:
        """
        Downloads model to cache.
        :param model_path: The located in bucket.
        :param bucket_name: The name of the bucket containing path to model.
        :return: The path to the downloaded model.
        """
        storage = SupportedCloudStorage.get_storage()
        if not storage.exists(model_path, bucket_name):
            raise Exception(f"Model does not exist at path: {model_path}")
        model_path = os.path.join(MODEL_CACHE_PATH, model_path)
        storage.copy(model_path, model_path, bucket_name)
        return model_path
