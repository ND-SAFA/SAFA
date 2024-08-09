from typing import Any, Dict

from datasets import load_dataset
from transformers import PreTrainedTokenizer

from common_resources.tools.constants.hugging_face_constants import INPUT_IDS_PARAM, TEXT_PARAM, TRAIN_PARAM
from common_resources.tools.util.list_util import ListUtil
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.llm.model_manager import ModelManager


class PreTrainDataset(iDataset):

    def __init__(self, training_file_path: str, block_size: int, **kwargs):
        """
        Represents a pretraining dataset
        :param training_file_path: the path to the file containing training examples
        :param block_size: the size to split the concatenated text into smaller chunks
        :param kwargs: any additional parameters used in the dataset
        """
        self.training_file_path = training_file_path
        self.block_size = block_size
        self.kwargs = kwargs

    def to_hf_dataset(self, model_manager: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_manager: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """
        tokenizer = model_manager.get_tokenizer()
        input_id_parser = self.create_input_id_parser(tokenizer, self.block_size)
        dataset = load_dataset(TEXT_PARAM, data_files={TRAIN_PARAM: self.training_file_path})
        dataset = dataset.map(input_id_parser, batched=True, remove_columns=[TEXT_PARAM], desc="Tokenizing dataset")
        return dataset[TRAIN_PARAM]

    def as_creator(self, project_path: str):
        """
        Pre train dataset cannot be converted to creator
        :param project_path: Ignored.
        """
        raise NotImplementedError("Pre train dataset cannot be converted to creator.")

    @staticmethod
    def create_input_id_parser(tokenizer: PreTrainedTokenizer, batch_size: int):
        """
        Creates a function that will parse texts into input ids.
        :param tokenizer: The tokenizer used to convert text into input ids.
        :param batch_size: The size of each batch of input ids.
        :return: The parsing function.
        """

        def parse_into_input_ids(texts: Dict):
            """
            Tokenizes texts and batches texts.
            :param texts: The texts to tokenize.
            :return: Dictionary containing input ids.
            """
            all_input_ids = []
            tokenizer_output = tokenizer(texts[TEXT_PARAM], add_special_tokens=True)[INPUT_IDS_PARAM]
            for input_ids in tokenizer_output:
                all_input_ids.extend(input_ids)
                all_input_ids.append(tokenizer.sep_token_id)
            batches = ListUtil.batch(all_input_ids, batch_size)
            return {INPUT_IDS_PARAM: batches}

        return parse_into_input_ids
