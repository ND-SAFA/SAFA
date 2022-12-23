import math
from typing import List, Tuple, Union

import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.dataset import TensorDataset

from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.trace_dataset import TraceDataset
from models.model_generator import ModelGenerator
from train.trace_args import TraceArgs
from util.file_util import FileUtil

UNLABELED_CLASS = 2
BINARY_LABEL_LIST = [0, 1, UNLABELED_CLASS]
LabeledExample = Tuple[str, str, int]
UnlabeledExample = Tuple[str, None]
Example = Union[LabeledExample, UnlabeledExample]


class GanDatasetConverter:

    def __init__(self, trace_args: TraceArgs, train_dataset: TraceDataset, pre_train_dataset: PreTrainDataset = None,
                 label_list: List = None):
        """
        Responsible for creating a data that the GAN will understand from a csv file containing two columns
        (text, label) where text contains the concatenated source and target artifacts. The label is either 0 or 1
        representing traced or not traced.
        """
        self.trace_args = trace_args
        self.labeled_examples = self.create_labeled_examples(train_dataset)
        self.unlabeled_examples = self.create_unlabeled_exampled(pre_train_dataset) if pre_train_dataset else None
        self.label_list = label_list if label_list else BINARY_LABEL_LIST

    def to_gan_dataset(self, model_generator: ModelGenerator) -> DataLoader:
        """
        Creates dataloader containing labeled and unlabeled examples for gan.
        :return:
        :rtype:
        """
        label_map = {}
        for (i, label) in enumerate(self.label_list):
            label_map[label] = i

        # 1. The labeled (train) data is assigned with a mask set to True
        input_examples = self.labeled_examples
        label_masks = np.ones(len(self.labeled_examples), dtype=bool)

        # If unlabeled examples are available then assign with a mask set to False
        if self.unlabeled_examples:
            input_examples = input_examples + self.unlabeled_examples
            tmp_masks = np.zeros(len(self.unlabeled_examples), dtype=bool)
            label_masks = np.concatenate([label_masks, tmp_masks])

        # Count the percentage of labeled examples
        label_mask_rate = GanDatasetConverter.calculate_mask_rate(input_examples, label_masks)

        # if required it applies the balance
        examples = GanDatasetConverter.balance_examples(
            input_examples,
            label_mask_rate,
            label_masks,
            self.trace_args.apply_balance)

        # Generate input examples to the Transformer
        input_ids, label_id_array, label_mask_array, input_mask_array = self.tokenize_examples(examples, label_map,
                                                                                               model_generator)
        tensor_dataset = self.to_tensor_dataset(input_ids, label_id_array, label_mask_array, input_mask_array)

        # Building the DataLoader
        sampler = RandomSampler if self.trace_args.shuffle else SequentialSampler
        return DataLoader(
            tensor_dataset,  # The training samples.
            sampler=sampler(tensor_dataset),
            batch_size=self.trace_args.train_batch_size)  # Trains with this batch size.

    def tokenize_examples(self, examples, label_map, model_generator: ModelGenerator):
        input_ids = []
        label_id_array = []
        label_mask_array = []
        input_mask_array = []
        for (text, label_mask) in examples:
            if label_mask is None or not label_mask:  # no label use single text encoding
                encoded_sent = model_generator.get_feature(text=text[0], add_special_tokens=True)
            else:  # if label use sequence encoding
                encoded_sent = model_generator.get_feature(text=text[0], text_pair=text[1], add_special_tokens=True)
            label = UNLABELED_CLASS if text[-1] not in label_map else label_map[text[-1]]
            input_ids.append(encoded_sent['input_ids'])
            label_id_array.append(label)
            label_mask_array.append(label_mask)

        for sent in input_ids:
            attention_mask = [int(token_id > 0) for token_id in sent]
            input_mask_array.append(attention_mask)
        return input_ids, label_id_array, label_mask_array, input_mask_array

    @staticmethod
    def to_tensor_dataset(input_ids, label_id_array, label_mask_array, input_mask_array):

        # Convertion to Tensor
        input_ids = torch.tensor(input_ids)
        input_mask_array = torch.tensor(input_mask_array)
        label_id_array = torch.tensor(label_id_array, dtype=torch.long)
        label_mask_array = torch.tensor(label_mask_array)
        # Building the TensorDataset
        return TensorDataset(input_ids, input_mask_array, label_id_array, label_mask_array)

    @staticmethod
    def calculate_mask_rate(input_examples, label_masks):
        num_labeled_examples = 0
        for label_mask in label_masks:
            if label_mask:
                num_labeled_examples += 1
        label_mask_rate = num_labeled_examples / len(input_examples)
        return label_mask_rate

    @staticmethod
    def balance_examples(input_examples, label_mask_rate, label_masks, balance_label_examples: bool):
        new_examples = []
        for index, ex in enumerate(input_examples):
            new_samples = GanDatasetConverter.resample_example(
                ex,
                label_masks[index],
                label_mask_rate,
                balance_label_examples,
            )
            new_examples.extend(new_samples)
        return new_examples

    @staticmethod
    def resample_example(example: Example, label: Union[int, None], label_mask_rate: float, should_balance: bool, ) -> \
            List[Tuple[Example, Union[int, None]]]:
        """

        :param example: The example to resample
        :param label: The label of the example
        :param label_mask_rate:
        :param should_balance: Flag overriding balance operation
        :return:
        :rtype:
        """
        new_examples = []
        if label_mask_rate == 1 or not should_balance:
            new_examples.append((example, label))
        else:
            # IT SIMULATE A LABELED EXAMPLE
            if label:
                balance = int(1 / label_mask_rate)
                balance = int(math.log(balance, 2))
                if balance < 1:
                    balance = 1
                for b in range(0, int(balance)):
                    new_examples.append((example, label))
            else:
                new_examples.append((example, label))
        return new_examples

    @staticmethod
    def create_labeled_examples(trace_dataset: TraceDataset) -> List[LabeledExample]:
        """
        Creates a set of labeled examples from trace links in data.
        :param trace_dataset: The data whose trace links are converted to labeled examples.
        :return: List of labeled example representing trace links.
        """
        labeled_examples: List[LabeledExample] = []
        for trace_id, trace in trace_dataset.links.items():
            trace_label = 1 if trace.is_true_link else 0
            labeled_examples.append((trace.source_body.token, trace.target.token, trace_label))
        return labeled_examples

    @staticmethod
    def create_unlabeled_exampled(pre_training_dataset: PreTrainDataset) -> List[UnlabeledExample]:
        """
        Reads data and creates sets of unlabeled examples per line in file.
        :param pre_training_dataset: The data containing pre-training file.
        :return: List of unlabeled examples.
        """
        pre_training_file = FileUtil.read_file(pre_training_dataset.training_file_path)
        labeled_examples: List[UnlabeledExample] = []

        for line in pre_training_file.split("\n"):  # TODO : remove assumption that file must be separated by newlines
            labeled_examples.append((line, None))
        return labeled_examples
