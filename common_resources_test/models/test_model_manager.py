import mock
from mock import patch
from transformers import BertPreTrainedModel
from transformers.modeling_utils import PreTrainedModel
from transformers.models.auto import AutoModelForSequenceClassification
from transformers.models.auto.tokenization_auto import AutoTokenizer

from common_resources.llm.model_manager import ModelManager
from common_resources_test.base_tests.base_test import BaseTest


class TestTokenizer:
    model_max_length = 5


class TestModelManager(BaseTest):

    def test_get_encoder_layers(self):
        model: BertPreTrainedModel = AutoModelForSequenceClassification.from_pretrained(BaseTest.BASE_TEST_MODEL)
        manager = self.get_model_manager()
        layers = manager.get_encoder_layers(model)
        self.assertEqual(len(layers), BaseTest.BASE_MODEL_LAYERS)

    def test_freeze_layers(self):
        layers2freeze = [-2, 0]
        model = AutoModelForSequenceClassification.from_pretrained(BaseTest.BASE_TEST_MODEL)
        manager = self.get_model_manager()
        manager._freeze_layers(model, layers2freeze)
        layers = manager.get_encoder_layers(model)
        for layer_no in layers2freeze:
            layer = layers[layer_no]
            for param in layer:
                self.assertFalse(param.requires_grad)

    @patch.object(ModelManager, '_load_model')
    def test_get_model(self, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = PreTrainedModel
        test_generator = self.get_model_manager()
        test_generator.get_model()
        self.assertTrue(load_model_mock.called)

        # second time calling get_model should not call load model
        load_model_mock.called = False
        test_generator.get_model()
        self.assertFalse(load_model_mock.called)

    @patch.object(AutoTokenizer, 'from_pretrained')
    def test_get_tokenizer(self, from_pretrained_mock: mock.MagicMock):
        test_generator = self.get_model_manager()
        test_generator.get_tokenizer()
        self.assertTrue(from_pretrained_mock.called)

        # second time calling get_tokenizer should not call from_pretrained
        from_pretrained_mock.called = False
        test_generator.get_tokenizer()
        self.assertFalse(from_pretrained_mock.called)

    @patch.object(ModelManager, 'get_tokenizer')
    def test_set_max_seq_length_less_than_model_max(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = TestTokenizer
        test_generator = self.get_model_manager()
        test_generator.set_max_seq_length(2)

        self.assertEqual(test_generator._max_seq_length, 2)

    @patch.object(ModelManager, 'get_tokenizer')
    def test_set_max_seq_length_greater_than_model_max(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = TestTokenizer
        test_generator = self.get_model_manager()
        test_generator.set_max_seq_length(6)

        self.assertEqual(test_generator._max_seq_length, 5)

    def get_model_manager(self):
        return ModelManager("path")

    @patch.object(ModelManager, 'get_tokenizer')
    def test_get_feature_with_return_token_type_ids(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()

        test_model_generator = self.get_model_manager()
        feature = test_model_generator.get_feature(text="token", return_token_type_ids=True)
        self.assertIn("token_type_ids", feature)

    @patch.object(ModelManager, 'get_tokenizer')
    def test_get_feature_without_return_token_type_ids(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()

        test_model_generator = self.get_model_manager()
        feature = test_model_generator.get_feature(text="token", return_token_type_ids=False)
        self.assertNotIn("token_type_ids", feature)
