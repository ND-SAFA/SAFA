from transformers.models.electra.modeling_electra import ElectraClassificationHead, ElectraModel, ElectraPreTrainedModel

from models.base_models import single_model_forward_pass


class ElectraTraceSingle(ElectraPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.electra = ElectraModel(config)
        self.cls = ElectraClassificationHead(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask, token_type_ids, labels=None, **kwargs):
        return single_model_forward_pass(
            model=self.electra,
            cls_header=self.cls,
            num_labels=self.config.num_labels,
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            labels=labels,
            kwargs=kwargs,
        )
