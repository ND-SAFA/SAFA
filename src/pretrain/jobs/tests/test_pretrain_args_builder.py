from mock import patch

from common.models.model_properties import ModelSize
from pretrain.data.corpuses.domain import Domain
from pretrain.jobs.pretrain_args_builder import PretrainArgBuilder
from test.base_test import BaseTest


class TestPretrainArgsBuilder(BaseTest):
    EXPECTED_VALUES = {"model_name": "electra_trace_single",
                       "model_size": ModelSize.BASE,
                       "output_dir": "output",
                       "corpus_dir": "corpus",
                       "domain": Domain.BASE}
    EXPECTED_VALUES["model_path"] = "google/electra-" + EXPECTED_VALUES["domain"].value + "-discriminator"

    @patch("pretrain.electra.configure_pretraining.PretrainingConfig.__init__")
    def test_build(self, mock):
        test_pretrain_args_buidler = self.get_test_pretrain_arg_builder()
        args = test_pretrain_args_buidler.build()
        self.assertEquals(args.model_generator.model_name.lower(), self.EXPECTED_VALUES["model_name"])
        self.assertEquals(args.model_generator.model_path, self.EXPECTED_VALUES["model_path"])
        self.assertEquals(args.model_generator.model_size, self.EXPECTED_VALUES["model_size"])
        self.assertEquals(args.output_dir, self.EXPECTED_VALUES["output_dir"])
        self.assertEquals(args.corpus_dir, self.EXPECTED_VALUES["corpus_dir"])

    def get_test_pretrain_arg_builder(self):
        return PretrainArgBuilder(output_path=self.EXPECTED_VALUES["output_dir"],
                                  corpus_dir=self.EXPECTED_VALUES["corpus_dir"],
                                  domain=self.EXPECTED_VALUES["domain"], model_size=self.EXPECTED_VALUES["model_size"])
