from transformers.models.bert.tokenization_bert import BertTokenizer
import mock
from test.config.paths import TEST_VOCAB_FILE


def get_test_tokenizer():
    tokenizer = BertTokenizer(vocab_file=TEST_VOCAB_FILE)
    tokenizer._convert_token_to_id = mock.MagicMock(return_value=24)
    return tokenizer