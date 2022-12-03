import mock
from mock import patch
from transformers.modeling_utils import PreTrainedModel
from transformers.models.auto.tokenization_auto import AutoTokenizer

from test.base_test import BaseTest
from models.base_models.bert_trace_siamese import BertTraceSiamese
from models.base_models.supported_base_model import SupportedBaseModel
from models.model_generator import ModelGenerator
from models.model_properties import ModelArchitectureType


class TestTokenizer:
    model_max_length = 5


class TestModelGenerator(BaseTest):

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

        # second time calling get_tokenizer should not call from_pretrained
        from_pretrained_mock.called = False
        test_generator.get_tokenizer()
        self.assertFalse(from_pretrained_mock.called)

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
        return ModelGenerator("path")

    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_get_feature_with_return_token_type_ids(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()

        test_model_generator = self.get_test_model_generator()
        feature = test_model_generator.get_feature(text="token", return_token_type_ids=True)
        self.assertIn("token_type_ids", feature)

    @patch.object(ModelGenerator, 'get_tokenizer')
    def test_get_feature_without_return_token_type_ids(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()

        test_model_generator = self.get_test_model_generator()
        feature = test_model_generator.get_feature(text="token", return_token_type_ids=False)
        self.assertNotIn("token_type_ids", feature)
