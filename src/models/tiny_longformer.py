from transformers import LongformerForSequenceClassification


class TinyLongformer(LongformerForSequenceClassification):

    def __init__(self, config):
        config.intermediate_size = 3
        config.hidden_size = 24
        super().__init__(config)
