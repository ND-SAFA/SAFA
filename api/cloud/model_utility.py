import os

from api_constants import MODEL_CACHE_PATH
from cloud.supported_cloud_storage import SupportedCloudStorage


class CloudUtility:
    @staticmethod
    def download_model(model: str) -> str:
        """
        Downloads model to cache.
        :param model: The located in bucket.
        :return: The path to the downloaded model.
        """
        storage = SupportedCloudStorage.get_storage()
        if not storage.exists(model):
            raise Exception(f"Model does not exist at path: {model}")
        model_path = os.path.join(MODEL_CACHE_PATH, model)
        storage.copy(model, model_path)
        return model_path
