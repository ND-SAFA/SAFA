from copy import deepcopy
from unittest import mock
from unittest.mock import patch

from data.samplers.balanced_batch_sampler import BalancedBatchSampler
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest


class TestBalancedBatchSampler(BaseTraceTest):
    DATASET = BaseTraceTest.get_trace_dataset()

    def test_iter(self):
        batch_size = 4
        sampler = self.get_sampler(batch_size=batch_size)
        indices_for_epochs = [[], []]
        for i in iter(sampler):
            indices_for_epochs[0].append(i)
        for i in iter(sampler):
            indices_for_epochs[1].append(i)
        for epoch_indices in indices_for_epochs:
            self.assertEquals(len(self.DATASET.pos_link_ids) * 2, len(epoch_indices))
            self.assert_balanced_batches_in_sample(epoch_indices, batch_size)
        self.assertNotEqual(*indices_for_epochs)

    def test_get_pos_neg_link_indices(self):
        sampler = self.get_sampler()
        ordered_links = self.DATASET.get_ordered_links()
        expected_pos_link_indices = [i for i, link in enumerate(ordered_links) if link.is_true_link]
        expected_neg_link_indices = [i for i, link in enumerate(ordered_links) if not link.is_true_link]
        pos_link_indices, neg_link_indices = sampler._get_pos_neg_link_indices(sampler.data_source)
        self.assertListEqual(expected_pos_link_indices, pos_link_indices)
        self.assertListEqual(expected_neg_link_indices, neg_link_indices)

    def test_get_links_for_balanced_batches(self):
        batch_sizes = [i for i in range(2, 12)]
        for batch_size in batch_sizes:
            sampler = self.get_sampler(batch_size=batch_size)
            result = sampler._get_link_indices_for_balanced_batches()
            self.assert_balanced_batches_in_sample(result, batch_size)

    def assert_balanced_batches_in_sample(self, sample_indices, batch_size):
        neg_link_ids = deepcopy(self.DATASET.neg_link_ids)
        pos_link_ids = deepcopy(self.DATASET.pos_link_ids)
        selected_link_ids = [link.id for link in self.DATASET.get_ordered_links()]
        n_total_pos, n_total_neg = 0, 0
        n_batch_pos, n_batch_neg = 0, 0
        for i, link_index in enumerate(sample_indices):
            link_id = selected_link_ids[link_index]
            if i % batch_size == 0:
                self.assertLessEqual(abs(n_batch_pos - n_batch_neg), 1)
                n_batch_pos, n_batch_neg = 0, 0
            if link_id in neg_link_ids:
                neg_link_ids.remove(link_id)
                n_total_neg += 1
                n_batch_neg += 1
                continue
            if link_id in pos_link_ids:
                pos_link_ids.remove(link_id)
                n_total_pos += 1
                n_batch_pos += 1
                continue
            self.fail(f'Link {i}/{len(selected_link_ids)} was selected too many times')
        self.assertEquals(0, len(pos_link_ids))  # use all pos links
        self.assertLessEqual(abs(n_total_pos - n_total_neg), 1)

    @patch.object(ModelManager, "get_tokenizer")
    def get_sampler(self, get_tokenizer_mock: mock.MagicMock, batch_size: int = 4):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
        return BalancedBatchSampler(data_source=self.DATASET.to_trainer_dataset(model_generator), batch_size=batch_size)
