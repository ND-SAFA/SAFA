from enum import Enum

from models.bert_trace_siamese import BertTraceSiameseModelGenerator
from models.bert_trace_single import BertTraceSingleModelGenerator
from models.electra_trace_single import ElectraTraceSingleModelGenerator


class SupportedModelIdentifier(Enum):
    BERT_TRACE_SIAMESE = "bert_trace_siamese"
    BERT_TRACE_SINGLE = "bert_trace_single"
    ELECTRA_TRACE_SINGLE = "electra"


MODEL_GENERATORS = {SupportedModelIdentifier.BERT_TRACE_SINGLE: BertTraceSingleModelGenerator,
                    SupportedModelIdentifier.BERT_TRACE_SIAMESE: BertTraceSiameseModelGenerator,
                    SupportedModelIdentifier.ELECTRA_TRACE_SINGLE: ElectraTraceSingleModelGenerator}
