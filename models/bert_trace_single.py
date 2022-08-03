from typing import Type

from transformers import AutoModel, BertPreTrainedModel
from transformers.modeling_utils import PreTrainedModel
from transformers.models.electra.modeling_electra import (
    ElectraClassificationHead,
)

from models.abstract_model_generator import AbstractModelGenerator, ArchitectureType
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


class BertTraceSingleModelGenerator(AbstractModelGenerator):

    @property
    def base_model_class(self) -> Type[PreTrainedModel]:
        return BertTraceSingle

    @property
    def arch_type(self) -> ArchitectureType:
        return ArchitectureType.SINGLE

    # TODO
    def get_model_path(self) -> str:
        pass
