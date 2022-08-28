from transformers import RobertaForSequenceClassification


class BertTraceSingle(RobertaForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)
   