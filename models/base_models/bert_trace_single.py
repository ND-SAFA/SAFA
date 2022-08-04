from transformers import AutoModel, BertPreTrainedModel
from transformers.models.electra.modeling_electra import (
    ElectraClassificationHead,
)


from models.single_model_forward_pass import single_model_forward_pass


class BertTraceSingle(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.bert = AutoModel.from_config(config)
        self.cls = ElectraClassificationHead(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask, token_type_ids, labels=None, **kwargs):
        return single_model_forward_pass(
            model=self.bert,
            cls_header=self.cls,
            num_labels=self.config.num_labels,
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            labels=labels,
            kwargs=kwargs,
        )

