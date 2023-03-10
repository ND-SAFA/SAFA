import os
import sys
import time
from pathlib import Path
from typing import Dict, Tuple, Union, List

import torch
from fairscale.nn.model_parallel.initialize import initialize_model_parallel
from transformers.modeling_utils import PreTrainedModel


from models.llama.modeling_llama import LLaMAPreTrainedModel
from models.llama.configuration_llama import LLaMAConfig
from models.llama.tokenization_llama import LLaMATokenizer
from models.model_manager import ModelManager
from util.json_util import JsonUtil


class LLaMAModelManager(ModelManager):

    def __init__(self, model_path: str, max_seq_len: int = 512, max_batch_size: int = 32):
        """
        Handles loading model and related functions
        :param model_path: The path to the model
        :param max_seq_len: The maximum sequence length for tokenization
        :param max_batch_size: The maximum size of the batch
        """
        super().__init__(str(model_path))
        # self.ckpt_dir = ckpt_dir
        # self._max_seq_length = max_seq_len
        #params = self._load_params(ckpt_dir)
        #self.model_args = ModelArgs(max_seq_len=max_seq_len, max_batch_size=max_batch_size, **params)

    @staticmethod
    def setup_model_parallel() -> Tuple[int, int]:
        """
        Setups the model parallelization
        :return: The local rank and world size
        """
        local_rank = int(os.environ.get("LOCAL_RANK", -1))
        world_size = int(os.environ.get("WORLD_SIZE", -1))

        torch.distributed.init_process_group("nccl")
        initialize_model_parallel(world_size)
        torch.cuda.set_device(local_rank)

        # seed must be the same in all processes
        torch.manual_seed(1)
        return local_rank, world_size

    @staticmethod
    def _load_params(ckpt_dir: str) -> Dict:
        """
        Loads the additional parameters for model arguments
        :param ckpt_dir: The path to the directory containing checkpoints
        :return: A dictionary of paramters for model argumetns
        """
        params_path = str(Path(ckpt_dir).joinpath("params.json"))
        return JsonUtil.read_json_file(params_path)

    @staticmethod
    def _get_checkpoint_path(ckpt_dir: str, world_size: int, local_rank: int) -> Path:
        """
        Gets the current checkpoint path
        :param ckpt_dir: The path to the checkpoint directory
        :param world_size: The number of processes in the current process group
        :param local_rank: The rank of the local process
        :return: The path to the current checkpoint
        """
        checkpoints = sorted(Path(ckpt_dir).glob("*.pth"))
        assert world_size == len(checkpoints), f"Loading a checkpoint for MP={len(checkpoints)} but world size is {world_size}"
        return checkpoints[local_rank]

    def _load_model(self):
        self.__config = LLaMAConfig.from_pretrained(self.model_path)
        model = LLaMAPreTrainedModel.from_pretrained(self.model_path, config=self.__config)
        if self.layers_to_freeze:
            self._freeze_layers(model, self.layers_to_freeze)
        return model

    def get_tokenizer(self) -> LLaMATokenizer:
        """
        Gets the pretrained Tokenizer
        :return: the Tokenizer
        """
        if self._tokenizer is None:
            self.__tokenizer = LLaMATokenizer.from_pretrained(self.model_path)
        return self.__tokenizer

    def get_feature(self, return_token_type_ids: bool = False, text: Union[str, List[str]] = None,
                    text_pair: Union[str, List[str]] = None, **kwargs) -> Dict:
        """
        Method to get the feature for the model
        :param return_token_type_ids: if True, returns the token type ids
        :param text: The text of 1 artifact to encode
        :param text_pair: The text of the 2nd artifact in the pair to encode
        :param kwargs: other arguments for tokenizer
        :return: feature name, value mappings
        """
        assert text and text_pair, "text and text_pair must be supplied for llama tokenization"
        text = [text] if not isinstance(text, List) else text
        text_pair = [text_pair] if not isinstance(text_pair, List) else text_pair
        assert len(text) == len(text_pair), "Must include the same number of text and text pairs"
        tokenizer = self.get_tokenizer()
        prompts = []
        for i, source in enumerate(text):
            target = text_pair[i]
            prompts.append(f"Source: {source} \nTarget: {target}")
        return tokenizer(text=prompts)