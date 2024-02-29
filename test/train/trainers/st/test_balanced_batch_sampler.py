from typing import List
from unittest import TestCase

from sentence_transformers import InputExample

from tgen.core.trainers.st.balanced_batch_sampler import BalancedBatchSampler


class TestBalancedBatchSampler(TestCase):

    def test_interface(self):
        examples = self.create_examples(4, 2)
        sampler = BalancedBatchSampler(examples, batch_size=4)
        self.assertEqual(1, len(sampler))
        self.assertEqual(1, sampler.n_batches)
        for batch in sampler:
            n_negative = len([i for i in batch if examples[i].label == 0])
            n_positive = len([i for i in batch if examples[i].label == 0])
            self.assertEqual(n_negative, n_positive)

    @staticmethod
    def create_examples(n_neg: int, n_pos: int) -> List[InputExample]:
        """
        Creates examples consisting of negative and positive labels.
        :param n_neg: Number of examples with negative labels.
        :param n_pos: Number of examples with positive labels.
        :return: Number of examples.
        """
        examples = []
        examples += [InputExample(texts=["A", "B"], label=0) for i in range(n_neg)]
        examples += [InputExample(texts=["A", "B"], label=1) for i in range(n_pos)]
        return examples
