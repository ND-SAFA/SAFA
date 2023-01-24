import random

from torch.utils.data.sampler import Sampler
from typing import Iterator, List, Tuple, Any, Dict

from data.datasets.data_key import DataKey
from util.general_util import ListUtil


class BalancedBatchSampler(Sampler[int]):

    def __init__(self, data_source: List[Dict[str, Any]], batch_size: int) -> None:
        """
        Sampler used for creating balanced batches
        :param data_source: the dataset to use
        :param batch_size: the size of the batch
        """
        self.data_source = data_source
        self.batch_size = batch_size
        self.pos_link_indices, self.neg_link_indices = self._get_pos_neg_link_indices(data_source)

    def _get_link_indices_for_balanced_batches(self) -> List[int]:
        """
        Gets links indices to create balanced batches
        :return: a list of ordered link indices
        """
        n_links_per_batch, rem_per_batch = divmod(self.batch_size, 2)
        links_indices = []

        def add_batch(batch):
            random.shuffle(batch)
            links_indices.extend(batch)

        pos_start, neg_start = 0, 0
        while pos_start < len(self.pos_link_indices):
            pos_links, pos_start = ListUtil.get_n_items_from_list(self.pos_link_indices, n_items=n_links_per_batch,
                                                                  init_index=pos_start)
            neg_links, neg_start = ListUtil.get_n_items_from_list(self.neg_link_indices, n_items=len(pos_links), init_index=neg_start)
            new_batch = pos_links + neg_links
            if rem_per_batch > 0:
                if pos_start <= neg_start:
                    extra_links, pos_start = ListUtil.get_n_items_from_list(self.pos_link_indices, n_items=rem_per_batch,
                                                                            init_index=pos_start)
                else:
                    extra_links, neg_start = ListUtil.get_n_items_from_list(self.neg_link_indices, n_items=rem_per_batch,
                                                                            init_index=neg_start)
                new_batch += extra_links
            add_batch(new_batch)
        return links_indices

    @staticmethod
    def _get_pos_neg_link_indices(data_source: List[Dict[str, Any]]) -> Tuple[List[int], List[int]]:
        """
        Gets the list of positive and negative link indices from the original data source
        :param data_source: the dataset to use
        :return: the list of positive link indices and negative link indices
        """
        pos_link_indices = []
        neg_link_indices = []
        for i, data in enumerate(data_source):
            if data[DataKey.LABEL_KEY] == 1:
                pos_link_indices.append(i)
            else:
                neg_link_indices.append(i)
        return pos_link_indices, neg_link_indices

    def _shuffle_indices(self) -> None:
        """
        Shuffles the positive and negative link indices
        :return: None
        """
        random.shuffle(self.pos_link_indices)
        random.shuffle(self.neg_link_indices)

    def __iter__(self) -> Iterator[int]:
        """
        Required method used to sample data so that batches are balanced
        :return: iterator with balanced batches
        """
        self._shuffle_indices()
        return iter(self._get_link_indices_for_balanced_batches())

    def __len__(self) -> int:
        """
        Length of the dataset to sample
        :return: the length of the dataset
        """
        return len(self.data_source)
