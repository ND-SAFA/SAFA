import gc
import os

import torch
from sentence_transformers import SentenceTransformer
from typing import Type

from tgen.common.constants import environment_constants
from tgen.common.logging.logger_manager import logger
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.param_specs import ParamSpecs


class ModelCache:
    MODEL_MAP = {}

    @staticmethod
    def get_model(model_name: str, model_type: Type[SentenceTransformer] = SentenceTransformer) -> SentenceTransformer:
        """
        Returns the model with given name.
        :param model_name: The name of the model.
        :param model_type: The type of model to get.
        :return: The model.
        """
        if model_name in ModelCache.MODEL_MAP:
            logger.info(f"Loading cached model: {model_name}")
            return ModelCache.MODEL_MAP[model_name]
        else:
            kwargs = {}
            use_cache = False
            if "cache_folder" in ParamSpecs.create_from_method(model_type.__init__).param_names:
                cache_dir = ModelCache.get_cache_dir()
                logger.info(f"Creating model {model_name} in cache.")
                kwargs = DictUtil.update_kwarg_values(kwargs, cache_folder=cache_dir)
                use_cache = True
            model = model_type(model_name, **kwargs)
            if use_cache:
                ModelCache.MODEL_MAP[model_name] = model
            return model

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
        logger.info("Clearing model cache.")
        ModelCache.MODEL_MAP = {}
        gc.collect()
        torch.cuda.empty_cache()
