from transformers import LongformerForSequenceClassification


class TinyLongformer(LongformerForSequenceClassification):

    def __init__(self, config):
        # config.intermediate_size = 100  # Dimensionality of the "intermediate" (often named feed-forward) layer in the Transformer encoder.
        # config.hidden_size = 12  # Dimensionality of the encoder layers and the pooler layer.

        config.num_hidden_layers = 1  # Number of hidden layers in the Transformer encoder.
        config.num_attention_heads = 1  # Number of attention heads for each attention layer in the Transformer encoder.
        config.attention_window = [512] * config.num_hidden_layers  # Size of an attention window around each token.
        super().__init__(config)
