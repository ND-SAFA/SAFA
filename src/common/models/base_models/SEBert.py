from transformers import BertForSequenceClassification


class SEBert(BertForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)
