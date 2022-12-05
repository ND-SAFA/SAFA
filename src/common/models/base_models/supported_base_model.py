from enum import Enum

from transformers import AutoModelForSequenceClassification

from common.models.base_models.bert_trace_siamese import BertTraceSiamese
from common.models.base_models.electra_trace_single import ElectraTraceSingle
from common.models.base_models.pl_bert import PLBert


class SupportedBaseModel(Enum):
    PL_BERT = PLBert
    NL_BERT = AutoModelForSequenceClassification
    BERT_TRACE_SIAMESE = BertTraceSiamese
    ELECTRA_TRACE_SINGLE = ElectraTraceSingle
