from transformers import ElectraPreTrainedModel
from transformers.models.electra.modeling_electra import ElectraClassificationHead, ElectraModel

from models.base_model_identifier import BaseModelIdentifier
from models.single_lm_forward import single_lm_forward


class ElectraTraceSingle(ElectraPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.electra = ElectraModel(config)
        self.cls = ElectraClassificationHead(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask, token_type_ids, labels=None, **kwargs):
        return single_lm_forward(
            model=self.electra,
            cls_header=self.cls,
            num_labels=self.config.num_labels,
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            labels=labels,
            kwargs=kwargs,
        )


class ElectraTraceSingleIdentifier(BaseModelIdentifier):

    @property
    def model_class(self):
        return ElectraTraceSingle

    @property
    def model_path(self):
        pass
