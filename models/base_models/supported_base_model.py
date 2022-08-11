from enum import Enum

from models.base_models.bert_trace_siamese import BertTraceSiamese
from models.base_models.bert_trace_single import BertTraceSingle
from models.base_models.electra_trace_single import ElectraTraceSingle


class SupportedBaseModel(Enum):
    BERT_TRACE_SINGLE = BertTraceSingle
    BERT_TRACE_SIAMESE = BertTraceSiamese
    ELECTRA_TRACE_SINGLE = ElectraTraceSingle
