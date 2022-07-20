from typing import Type

from transformers import ElectraPreTrainedModel
from transformers.models.electra.modeling_electra import ElectraClassificationHead, ElectraModel

from models.model_generator import BaseModelGenerator, ArchitectureType
from transformers.modeling_utils import PreTrainedModel
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


class ElectraTraceSingleModelGenerator(BaseModelGenerator):

    @property
    def base_model_class(self) -> Type[PreTrainedModel]:
        return ElectraTraceSingle

    # TODO
    @property
    def model_path(self) -> str:
        pass

    @property
    def arch_type(self) -> ArchitectureType:
        return ArchitectureType.SINGLE
