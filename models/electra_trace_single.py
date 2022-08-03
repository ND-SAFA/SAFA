from typing import Type

from transformers import ElectraPreTrainedModel
from transformers.modeling_utils import PreTrainedModel
from transformers.models.electra.modeling_electra import ElectraClassificationHead, ElectraModel

from models.abstract_model_generator import AbstractModelGenerator, ArchitectureType
from models.single_model_forward_pass import single_model_forward_pass


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


class ElectraTraceSingleModelGenerator(AbstractModelGenerator):

    @property
    def base_model_class(self) -> Type[PreTrainedModel]:
        return ElectraTraceSingle

    @property
    def arch_type(self) -> ArchitectureType:
        return ArchitectureType.SINGLE

    def get_model_name(self) -> str:
        return f"electra_{self.model_size.value}"

    # TODO
    def get_model_path(self) -> str:
        return f"google/electra-{self.model_size.value}-discriminator"
