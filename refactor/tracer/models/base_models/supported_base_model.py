from enum import Enum

from transformers import BertForMaskedLM

from tracer.models import BertTraceSiamese, ElectraTraceSingle, NLBert, PLBert


class SupportedBaseModel(Enum):
    PL_BERT = PLBert
    NL_BERT = NLBert
    BERT_TRACE_SIAMESE = BertTraceSiamese
    ELECTRA_TRACE_SINGLE = ElectraTraceSingle
    BERT_FOR_MASKED_LM = BertForMaskedLM
