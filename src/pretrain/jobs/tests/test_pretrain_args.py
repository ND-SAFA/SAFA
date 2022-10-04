from mock import patch

from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from pretrain.jobs.pretrain_args import PretrainArgs
from test.base_test import BaseTest


class TestPretrainArgs(BaseTest):

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
        return PretrainArgs(ModelGenerator(SupportedBaseModel.BERT_TRACE_SIAMESE, "path"), "output_path")
