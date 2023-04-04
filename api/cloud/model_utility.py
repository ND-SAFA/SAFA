import os

from api_constants import MODEL_CACHE_PATH
from cloud.supported_cloud_storage import SupportedCloudStorage


class CloudUtility:
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
