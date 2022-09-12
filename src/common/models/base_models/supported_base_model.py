from enum import Enum

from common.models.base_models.SEBert import SEBert
from common.models.base_models.bert_trace_siamese import BertTraceSiamese
from common.models.base_models.bert_trace_single import TBertSingle
from common.models.base_models.electra_trace_single import ElectraTraceSingle


class SupportedBaseModel(Enum):
    T_BERT_SINGLE = TBertSingle
    SE_BERT = SEBert
    BERT_TRACE_SIAMESE = BertTraceSiamese
    ELECTRA_TRACE_SINGLE = ElectraTraceSingle
