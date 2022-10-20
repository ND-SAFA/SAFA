from enum import Enum

from transformers import BertForMaskedLM

from tracer.models.base_models.nl_bert import NLBert
from tracer.models.base_models.pl_bert import PLBert
from tracer.models.base_models.electra_trace_single import ElectraTraceSingle
from tracer.models.base_models.bert_trace_siamese import BertTraceSiamese


class SupportedBaseModel(Enum):
    PL_BERT = PLBert
    NL_BERT = NLBert
    BERT_TRACE_SIAMESE = BertTraceSiamese
    ELECTRA_TRACE_SINGLE = ElectraTraceSingle
    BERT_FOR_MASKED_LM = BertForMaskedLM
