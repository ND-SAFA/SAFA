from transformers import BertForSequenceClassification


class NLBert(BertForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)
