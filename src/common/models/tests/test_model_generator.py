from django.test import TestCase
import mock
from mock import patch
from transformers.modeling_utils import PreTrainedModel
from transformers.models.auto.tokenization_auto import AutoTokenizer
from common.models.model_generator import ModelGenerator
from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_properties import ArchitectureType

from common.models.base_models.bert_trace_siamese import BertTraceSiamese


class TestTokenizer:
    model_max_length = 5


class TestModelGenerator(TestCase):
    TEST_BASE_MODEL = {
        "base_model_name": "bert_trace_siamese",
        "arch_type": ArchitectureType.SIAMESE,
        "supported_base_model": SupportedBaseModel.BERT_TRACE_SIAMESE,
        "base_model_class": BertTraceSiamese

    }

    def test_get_supported_base_model(self):
        supported_base_model = ModelGenerator.get_supported_base_model(self.TEST_BASE_MODEL["base_model_name"])
        self.assertEqual(supported_base_model, self.TEST_BASE_MODEL["supported_base_model"])

    def test_get_supported_base_model_with_unknown_model(self):
        self.assertRaises(NameError, lambda: ModelGenerator.get_supported_base_model("bert"))

    def test_get_model_architecture_type(self):
        arch_type = ModelGenerator._get_model_architecture_type(self.TEST_BASE_MODEL["base_model_name"])
        self.assertEqual(arch_type, self.TEST_BASE_MODEL["arch_type"])

    def test_get_model_architecture_type_with_unknown_type(self):
        arch_type = ModelGenerator._get_model_architecture_type("bert")
        self.assertEqual(arch_type, ArchitectureType.SINGLE)

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    def test_get_model(self, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = PreTrainedModel
        test_generator = self.get_test_model_generator()
        test_generator.get_model()
        self.assertTrue(load_model_mock.called)

        # second time calling get_model should not call load model
        load_model_mock.called = False
        test_generator.get_model()
        self.assertFalse(load_model_mock.called)

    @patch.object(AutoTokenizer, 'from_pretrained')
    def test_get_tokenizer(self, from_pretrained_mock: mock.MagicMock):
        test_generator = self.get_test_model_generator()
        test_generator.get_tokenizer()
        self.assertTrue(from_pretrained_mock.called)

    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_set_max_seq_length_less_than_model_max(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = TestTokenizer
        test_generator = self.get_test_model_generator()
        test_generator.set_max_seq_length(2)

        self.assertEquals(test_generator._max_seq_length, 2)

    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_set_max_seq_length_greater_than_model_max(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = TestTokenizer
        test_generator = self.get_test_model_generator()
        test_generator.set_max_seq_length(6)

        self.assertEquals(test_generator._max_seq_length, 5)

    def get_test_model_generator(self):
        return ModelGenerator(self.TEST_BASE_MODEL["base_model_name"], "path")
