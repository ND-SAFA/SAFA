import math
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.dataset import TensorDataset

from gan.gan_args import Examples, GanArgs

BINARY_LABEL_LIST = [0, 1]


class GanDataset:
    """
    Responsible for creating a dataset that the GAN will understand from a csv file containing two columns
    (text, label) where text contains the concatenated source and target artifacts. The label is either 0 or 1
    representing traced or not traced.
    """

    def __init__(self, args: GanArgs, tokenizer, label_list=BINARY_LABEL_LIST):
        self.args = args
        self.tokenizer = tokenizer
        self.labeled_examples = args.train_examples
        self.test_examples = args.test_examples
        self.unlabeled_examples = args.unlabeled_examples
        self.label_list = label_list

    def __add__(self, other: "GanDataset"):
        tokenizer = self.tokenizer
        combined_labeled_examples = self.labeled_examples + self.test_examples + other.labeled_examples + other.test_examples
        combined_unlabeled_examples = self.unlabeled_examples + other.unlabeled_examples
        combined_dataset = GanDataset(tokenizer, combined_labeled_examples, combined_unlabeled_examples)
        return combined_dataset

    def build(self):
        """
        Load the train dataset
        :return:
        :rtype:
        """
        label_map = {}
        for (i, label) in enumerate(self.label_list):
            label_map[label] = i

        train_examples = self.labeled_examples
        # The labeled (train) dataset is assigned with a mask set to True
        train_label_masks = np.ones(len(self.labeled_examples), dtype=bool)
        # If unlabel examples are available
        if self.unlabeled_examples:
            train_examples = train_examples + self.unlabeled_examples
            # The unlabeled (train) dataset is assigned with a mask set to False
            tmp_masks = np.zeros(len(self.unlabeled_examples), dtype=bool)
            train_label_masks = np.concatenate([train_label_masks, tmp_masks])

        train_dataloader = self.__generate_data_loader(self.args,
                                                       train_examples,
                                                       train_label_masks,
                                                       label_map,
                                                       self.tokenizer,
                                                       do_shuffle=True,
                                                       balance_label_examples=self.args.apply_balance)

        # ------------------------------
        #   Load the test dataset
        # ------------------------------
        # The labeled (test) dataset is assigned with a mask set to True
        test_label_masks = np.ones(len(self.test_examples), dtype=bool)

        test_dataloader = self.__generate_data_loader(self.args, self.test_examples, test_label_masks, label_map,
                                                      self.tokenizer,
                                                      do_shuffle=False,
                                                      balance_label_examples=False)

        return train_dataloader, test_dataloader, train_examples

    @staticmethod
    def __generate_data_loader(gan_args: GanArgs, input_examples: Examples, label_masks, label_map, tokenizer,
                               do_shuffle=False,
                               balance_label_examples=False):
        """
        Generate a Dataloader given the input examples, eventually masked if they are
        to be considered NOT labeled.
        :param input_examples: TODO
        :param label_masks: TODO
        :param label_map: TODO
        :param do_shuffle: TODO
        :param balance_label_examples: TODO
        :return:
        """
        examples = []

        # Count the percentage of labeled examples
        num_labeled_examples = 0
        for label_mask in label_masks:
            if label_mask:
                num_labeled_examples += 1
        label_mask_rate = num_labeled_examples / len(input_examples)

        # if required it applies the balance
        for index, ex in enumerate(input_examples):
            if label_mask_rate == 1 or not balance_label_examples:
                examples.append((ex, label_masks[index]))
            else:
                # IT SIMULATE A LABELED EXAMPLE
                if label_masks[index]:
                    balance = int(1 / label_mask_rate)
                    balance = int(math.log(balance, 2))
                    if balance < 1:
                        balance = 1
                    for b in range(0, int(balance)):
                        examples.append((ex, label_masks[index]))
                else:
                    examples.append((ex, label_masks[index]))

        # -----------------------------------------------
        # Generate input examples to the Transformer
        # -----------------------------------------------
        input_ids = []
        input_mask_array = []
        label_mask_array = []
        label_id_array = []

        # Tokenization
        for (text, label_mask) in examples:
            encoded_sent = tokenizer.encode(text[0], add_special_tokens=True, max_length=gan_args.max_seq_length,
                                            padding="max_length", truncation=True)
            input_ids.append(encoded_sent)
            label_id_array.append(label_map[text[1]])
            label_mask_array.append(label_mask)

        # Attention to token (to ignore padded input wordpieces)
        for sent in input_ids:
            att_mask = [int(token_id > 0) for token_id in sent]
            input_mask_array.append(att_mask)
        # Convertion to Tensor
        input_ids = torch.tensor(input_ids)
        input_mask_array = torch.tensor(input_mask_array)
        label_id_array = torch.tensor(label_id_array, dtype=torch.long)
        label_mask_array = torch.tensor(label_mask_array)

        # Building the TensorDataset
        dataset = TensorDataset(input_ids, input_mask_array, label_id_array, label_mask_array)

        if do_shuffle:
            sampler = RandomSampler
        else:
            sampler = SequentialSampler

        # Building the DataLoader
        return DataLoader(
            dataset,  # The training samples.
            sampler=sampler(dataset),
            batch_size=gan_args.batch_size)  # Trains with this batch size.

    @staticmethod
    def __get_examples(data_file_path: str) -> Examples:
        """
        Returns dataset examples for the GAN.
        :return: List of examples where each example contains the text being classified and the classification label.
        """
        data_df = pd.read_csv(data_file_path)
        examples = []
        for idx, series in data_df.iterrows():
            text = series["text"]
            label = series["label"]
            examples.append((text, label))
        return examples
