from enum import IntEnum, auto
from bert_trace_single import BertTraceSingleModelGenerator
from models.bert_trace_siamese import BertTraceSiameseModelGenerator
from models.electra_trace_single import ElectraTraceSingleModelGenerator


class SupportedModels(IntEnum):
    BERT_TRACE_SIAMESE = auto()
    BERT_TRACE_SINGLE = auto()
    ELECTRA_TRACE_SINGLE = auto()


MODEL_GENERATORS = {SupportedModels.BERT_TRACE_SINGLE: BertTraceSingleModelGenerator,
                    SupportedModels.BERT_TRACE_SIAMESE: BertTraceSiameseModelGenerator,
                    SupportedModels.ELECTRA_TRACE_SINGLE: ElectraTraceSingleModelGenerator}
