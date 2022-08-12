from django.test import TestCase
from mock import patch

from common.models.model_generator import ModelGenerator
from pretrain.jobs.pretrain_args import PretrainArgs


class TestPretrainArgs(TestCase):

    @patch("pretrain.electra.configure_pretraining.PretrainingConfig.__init__")
    def test_set_do_train_true(self, mock):
        pretrain_args = self.get_test_pretrain_args()
        pretrain_args.set_do_train(True)
        self.assertTrue(pretrain_args.do_train)
        self.assertFalse(pretrain_args.do_eval)

    @patch("pretrain.electra.configure_pretraining.PretrainingConfig.__init__")
    def test_set_do_train_false(self, mock):
        test_pretrain_args = self.get_test_pretrain_args()
        test_pretrain_args.set_do_train(False)
        self.assertFalse(test_pretrain_args.do_train)
        self.assertTrue(test_pretrain_args.do_eval)

    def get_test_pretrain_args(self):
        return PretrainArgs(ModelGenerator("bert_trace_siamese", "path"), "output_path")
