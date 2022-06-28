import enum
from bert_trace_single import BertTraceSingleIdentifier
from models.bert_trace_siamese import BertTraceSiameseIdentifier
from models.electra_trace_single import ElectraTraceSingleIdentifier


class SupportedModels(enum):
    BERT_TRACE_SIAMESE = 'bert_trace_siamese'
    BERT_TRACE_SINGLE = 'bert_trace_single'
    ELECTRA_TRACE_SINGLE = 'electra_trace_single'


MODEL_IDENTIFIERS = {SupportedModels.BERT_TRACE_SINGLE: BertTraceSingleIdentifier,
                     SupportedModels.BERT_TRACE_SIAMESE: BertTraceSiameseIdentifier,
                     SupportedModels.ELECTRA_TRACE_SINGLE: ElectraTraceSingleIdentifier}
