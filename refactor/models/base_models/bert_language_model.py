from transformers import BertForMaskedLM


class BertLanguageModel(BertForMaskedLM):
    def __init__(self, config):
        super().__init__(config)
