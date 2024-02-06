import numpy as np


class BalancedBatchSampler:
    def __init__(self, dataset, batch_size: int):
        self.indices = list(np.arange(len(dataset)))
        self.num_samples = len(dataset)
        self.labels = np.array([example.label for example in dataset])
        self.n_positive = len([s for s in self.labels if s != 0])
        self.batch_size = batch_size
        self.negative_indices = self.create_negative_indices()
        self.other_indices = self.create_other_indices()
        self.n_batches = int(min(len(self.other_indices), len(self.negative_indices)) // (self.batch_size / 2))

    def create_negative_indices(self):
        return [i for i in self.indices if self.labels[i] == 0]

    def create_other_indices(self):
        return [i for i in self.indices if self.labels[i] != 0]

    def select_negative(self, n_items: int):
        selected, self.negative_indices = self.select_indices(self.negative_indices, n_items, self.create_negative_indices)
        return selected

    def select_other(self, n_items: int):
        selected, self.other_indices = self.select_indices(self.other_indices, n_items, self.create_other_indices)
        return selected

    @staticmethod
    def select_indices(indices, n_items, create_indices_method):
        if n_items > len(indices):
            indices = create_indices_method()  # Recreate indices using the provided method

        selected = list(np.random.choice(indices, n_items, replace=False))
        indices = [index for index in indices if index not in selected]  # Efficient way to remove selected items
        return selected, indices  # Return both selected items and the updated indices list

    def __iter__(self):
        return self

    def __next__(self):
        n_negative = self.batch_size // 2
        n_pos = self.batch_size - n_negative
        batch_indices = self.select_negative(n_negative) + self.select_other(n_pos)
        np.random.shuffle(batch_indices)
        return batch_indices

    def __len__(self):
        return self.n_batches
