import os

from sentence_transformers import SentenceTransformer

from tgen.common.constants import environment_constants
from tgen.common.logging.logger_manager import logger


class ModelCache:
    MODEL_MAP = {}

    @staticmethod
    def get_model(model_name: str) -> SentenceTransformer:
        """
        Returns the model with given name.
        :param model_name: The name of the model.
        :return: The model.
        """
        if model_name in ModelCache.MODEL_MAP:
            return ModelCache.MODEL_MAP[model_name]
        else:
            cache_dir = ModelCache.get_cache_dir()
            logger.info(f"Loading model {model_name} from {cache_dir}")
            return SentenceTransformer(model_name, cache_folder=cache_dir)

    @staticmethod
    def get_cache_dir() -> str:
        """
        :return: Returns path to cache directory for the models.
        """
        cache_dir = os.environ.get("HF_DATASETS_CACHE", None)
        if cache_dir is None or environment_constants.IS_TEST or not os.path.exists(cache_dir):
            cache_dir = None
        return cache_dir

    @staticmethod
    def clear() -> None:
        """
        Creates the current model map.
        :return: None
        """
        ModelCache.MODEL_MAP = {}
