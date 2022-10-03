from transformers import RobertaForSequenceClassification


class PLBert(RobertaForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)
