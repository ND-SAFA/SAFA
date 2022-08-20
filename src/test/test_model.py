from transformers.models.bert.configuration_bert import BertConfig
from common.models.base_models.bert_trace_single import BertTraceSingle


def get_test_model():
    return BertTraceSingle(get_test_config())


def get_test_config():
    """
    Returns a tiny configuration by default.
    """
    return BertConfig(
        vocab_size=99,
        hidden_size=32,
        num_hidden_layers=5,
        num_attention_heads=4,
        intermediate_size=37,
        hidden_act="gelu",
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        max_position_embeddings=512,
        type_vocab_size=16,
        is_decoder=False,
        initializer_range=0.02,
    )
