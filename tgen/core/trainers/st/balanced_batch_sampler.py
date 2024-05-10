from typing import Iterator, List, Sequence, Tuple

import numpy as np
from sentence_transformers import InputExample


class BalancedBatchSampler:
    def __init__(self, input_examples: List[InputExample], batch_size: int):
        """
        Creates batches for training loop.
        :param input_examples: The total list of input examples.
        :param batch_size: The size of each batch.
        """
        self.indices, self.labels = BalancedBatchSampler.create_indices_and_labels(input_examples)
        self.num_samples = len(input_examples)
        self.non_negative_indices, self.negative_indices = self.create_indices(self.labels)
        self.n_positive = len(self.non_negative_indices)
        self.batch_size = batch_size
        self.n_batches = self.calculate_n_batches(batch_size, self.non_negative_indices, self.negative_indices)
        self.n_labels = 2  # for now..

    def __iter__(self) -> Iterator:
        """
        :return: Returns itself as the iterator.
        """
        return self

    def __next__(self):
        """
        Creates the next batch of data.
        :return: The indices of the data.
        """
        n_negative = self.batch_size // self.n_labels
        n_non_negative = self.batch_size - n_negative
        if n_negative > len(self.negative_indices) or n_non_negative > len(self.non_negative_indices):
            raise StopIteration
        batch_indices = self.select_negative(n_negative) + self.select_non_negative(n_non_negative)
        np.random.shuffle(batch_indices)
        return batch_indices

    def __len__(self):
        """
        :return: Returns the number of batches available.
        """
        return self.n_batches

    def reset(self) -> None:
        """
        Resets the available samples.
        :return: None.
        """
        self.non_negative_indices, self.negative_indices = self.create_indices(self.labels)

    def select_negative(self, n_items: int) -> List[int]:
        """
        Selects native indices for next batch. Updates negative indices with those unselected.
        :param n_items: The number of indices to select.
        :return: The indices of negative samples not chosen this epoch.
        """
        selected, self.negative_indices = self.randomly_select_indices(self.negative_indices, n_items)
        return selected

    def select_non_negative(self, n_items: int):
        """
        Selects non-negative indices for next batch. Updates non-negative indices with those remaining to be selected.
        :param n_items: The number of indices to select.
        :return: The selected indices.
        """
        selected, self.non_negative_indices = self.randomly_select_indices(self.non_negative_indices, n_items)
        return selected

    @staticmethod
    def calculate_n_batches(batch_size: int, *label_indices: List[int], ) -> int:
        """
        Calculates the maximum number of possible balanced batches.
        :param batch_size: The size of each batch.
        :param label_indices: The indices for each type of label to be balanced.
        :return: The maximum number of balanced batches.
        """
        n_labels = len(label_indices)
        label_sizes = [len(indices) for indices in label_indices]
        min_labels = min(*label_sizes)  # find labels that will run out first.
        return int(min_labels // (batch_size / n_labels))

    @staticmethod
    def create_indices_and_labels(input_examples: List[InputExample]) -> Tuple[List[int], List[int]]:
        """
        Creates list of indices and their corresponding labels.
        :param input_examples: The input examples to de-construct.
        :return: Indices and labels.
        """
        indices, labels = [], []
        for i, input_example in enumerate(input_examples):
            indices.append(i)
            labels.append(input_example.label)
        return indices, labels

    @staticmethod
    def create_indices(labels: Sequence[int]):
        """
        Finds indices containing non-negative labels and negative labels.
        :param labels: The list of labels.
        :return: List of indices for non-negative labels and negative ones.
        """
        other_labels = []
        negative_labels = []

        for i, label in enumerate(labels):
            if label == 0:
                negative_labels.append(i)
            else:
                other_labels.append(i)

        return other_labels, negative_labels

    @staticmethod
    def randomly_select_indices(indices: List[int], n_items: int) -> Tuple[List[int], List[int]]:
        """
        Randomly selects indices.
        :param indices: The indices to select from.
        :param n_items: How many indices to select.
        :return: The selected indices and the indices remaining.
        """
        if n_items > len(indices):
            raise Exception(f"Requested {n_items} but only have len{len(indices)} left...")
        selected = list(np.random.choice(indices, n_items, replace=False))
        indices = [index for index in indices if index not in selected]  # Efficient way to remove selected items
        return selected, indices  # Return both selected items and the updated indices list
