import random
from typing import Optional

from transformers import set_seed
import torch


class RandomUtil:

    CURRENT_SEED: Optional[int] = None

    @staticmethod
    def set_seed(random_seed: int) -> None:
        """
        Sets the random seed used for training
        :param random_seed: the random seed to use
        :return: None
        """
        random.seed(random_seed)
        set_seed(random_seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        RandomUtil.CURRENT_SEED = random_seed
