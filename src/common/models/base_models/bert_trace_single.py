from transformers import RobertaForSequenceClassification


class TBertSingle(RobertaForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)
