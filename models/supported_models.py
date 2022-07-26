from enum import IntEnum, auto
from bert_trace_single import BertTraceSingleModelGenerator
from models.bert_trace_siamese import BertTraceSiameseModelGenerator
from models.electra_trace_single import ElectraTraceSingleModelGenerator


class SupportedModels(IntEnum):
    BERT_TRACE_SIAMESE = "bert_trace_siamese"
    BERT_TRACE_SINGLE = "bert_trace_single"
    ELECTRA_TRACE_SINGLE = "electra"


MODEL_GENERATORS = {SupportedModels.BERT_TRACE_SINGLE.value: BertTraceSingleModelGenerator,
                    SupportedModels.BERT_TRACE_SIAMESE.value: BertTraceSiameseModelGenerator,
                    SupportedModels.ELECTRA_TRACE_SINGLE.value: ElectraTraceSingleModelGenerator}
